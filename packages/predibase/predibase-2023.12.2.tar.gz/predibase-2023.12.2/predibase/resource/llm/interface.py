import concurrent.futures
import functools
import os
import time
from dataclasses import dataclass, field
from pprint import pprint
from string import Formatter
from typing import Any, Dict, List, Optional, TYPE_CHECKING, Union

from dataclasses_json import config, dataclass_json, LetterCase

from predibase.resource import model as mdl
from predibase.resource.connection import get_dataset
from predibase.resource.dataset import Dataset
from predibase.resource.engine import Engine
from predibase.resource.llm.response import GeneratedResponse
from predibase.resource.llm.template import FinetuneTemplateCollection
from predibase.resource_util import build_model
from predibase.util import load_yaml

if TYPE_CHECKING:
    from predibase.pql.api import Session

_PATH_HERE = os.path.abspath(os.path.dirname(__file__))
_TEMPLATE_DIR = os.path.join(_PATH_HERE, "templates")


class HuggingFaceLLM:
    def __init__(self, session: "Session", model_name: str):
        self.session = session
        self.model_name = model_name

    def get_finetune_templates(self) -> FinetuneTemplateCollection:
        return FinetuneTemplateCollection(self)

    def deploy(
        self,
        deployment_name: str,
        engine_template: Optional[str] = None,
        hf_token: Optional[str] = None,
        auto_suspend_seconds: Optional[int] = None,
        max_input_length: Optional[int] = 1024,
        max_total_tokens: Optional[int] = 2048,
        max_batch_prefill_tokens: Optional[int] = 4096,
    ) -> "LLMDeploymentJob":
        # TODO: if model is an adapter add the base model from the adapter_config.json
        custom_args = [
            [arg[0], str(arg[1])]
            for arg in [
                ("--max-input-length", max_input_length),
                ("--max-total-tokens", max_total_tokens),
                ("--max-batch-prefill-tokens", max_batch_prefill_tokens),
            ]
            if arg[1] is not None
        ]
        custom_args = [element for sublist in custom_args for element in sublist]

        model_params = {
            "name": deployment_name,
            "modelName": self.model_name,
            "engineTemplate": engine_template,
            "scaleDownPeriod": auto_suspend_seconds,
            "source": "huggingface",
            "customArgs": custom_args,
        }

        if hf_token is not None:
            model_params["hfToken"] = hf_token

        llm_deployment_params = self.session.post_json(
            "/llms",
            json=model_params,
        )

        print("Deploying the model with the following params:")
        pprint(llm_deployment_params)

        return LLMDeploymentJob(deployment_name, self.session)

    def finetune(
        self,
        prompt_template: Optional[str] = None,
        target: Optional[str] = None,
        dataset: Optional[Union[str, Dataset]] = None,
        engine: Optional[Union[str, Engine]] = None,
        config: Optional[Union[str, Dict]] = None,
        repo: Optional[str] = None,
        epochs: Optional[int] = None,
        train_steps: Optional[int] = None,
        learning_rate: Optional[float] = None,
    ) -> "mdl.ModelFuture":
        if config is None:
            config = self.get_finetune_templates().default.to_config(prompt_template=prompt_template, target=target)
        else:
            if isinstance(config, str):
                config = load_yaml(config)

            if not isinstance(config, dict):
                raise ValueError(f"Invalid config type: {type(config)}, expected str or dict")

        # Apply first-class training parameters.
        if train_steps is not None and epochs is not None:
            raise ValueError("Cannot specify both train_steps and epochs.")
        if train_steps is not None:
            config["trainer"]["train_steps"] = train_steps
        if epochs is not None:
            config["trainer"]["epochs"] = epochs
        if learning_rate is not None:
            config["trainer"]["learning_rate"] = learning_rate

        if repo is None:
            # If no repo is specified, automatically construct the repo name from the dataset and model name.
            dataset_name = dataset.name if isinstance(dataset, Dataset) else dataset
            if "/" in dataset_name:
                _, dataset_name = dataset_name.split("/")

            model_name = self.model_name
            if "/" in model_name:
                _, model_name = model_name.split("/")

            repo = f"{model_name}-{dataset_name}"

        if "/" in repo:
            repo = repo.replace("/", "-")

        repo: "mdl.ModelRepo" = get_or_create_repo(self.session, repo)
        if dataset is None:
            # Assume the dataset is the same as the repo head
            md = repo.head().to_draft()
            md.config = config
        else:
            if isinstance(dataset, str):
                conn_name = None
                if "/" in dataset:
                    conn_name, dataset = dataset.split("/")
                dataset = get_dataset(self.session, dataset, connection_name=conn_name)
            md = repo.create_draft(config=config, dataset=dataset)

        return md.train_async(engine=engine)


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class _LLMDeployment:
    id: int = field(metadata=config(field_name="id"))
    tenant_id: int = field(metadata=config(field_name="tenantID"))
    uuid: str = field(metadata=config(field_name="uuid"))
    name: str = field(metadata=config(field_name="name"))
    description: Optional[str] = field(metadata=config(field_name="description"))
    model_name: str = field(metadata=config(field_name="modelName"))
    adapter_name: Optional[str] = field(metadata=config(field_name="adapterName"))
    num_shards: Optional[int] = field(metadata=config(field_name="numShards"))
    quantize: bool = field(metadata=config(field_name="quantize"))
    deployment_status: str = field(metadata=config(field_name="deploymentStatus"))

    prompt_template: str = field(metadata=config(field_name="promptTemplate"))
    min_replicas: int = field(metadata=config(field_name="minReplicas"))
    max_replicas: int = field(metadata=config(field_name="maxReplicas"))
    created: str = field(metadata=config(field_name="created"))
    updated: str = field(metadata=config(field_name="updated"))
    created_by_user_id: Optional[int] = field(metadata=config(field_name="createdByUserID"))
    scale_down_period: int = field(metadata=config(field_name="scaleDownPeriod"))
    error_text: Optional[str] = field(metadata=config(field_name="errorText"), default=None)
    dynamic_adapter_loading_enabled: bool = field(
        metadata=config(field_name="dynamicAdapterLoadingEnabled"),
        default=False,
    )


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class LLMDeploymentReadyResponse:
    name: str
    ready: bool


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class LLMDeploymentScaledResponse:
    name: str
    scaled: bool


class LLMDeployment:
    def __init__(
        self,
        session: "Session",
        name: str,
        # adapter can be a HuggingFaceLLM or mdl.Model
        adapter: Optional[Union["mdl.Model", HuggingFaceLLM]] = None,
        deployment_metadata: Optional[_LLMDeployment] = None,
    ):
        self.session = session
        self.name = name
        self.data = (
            _LLMDeployment.from_dict(self.session.get_json(f"/llms/{self.name}"))
            if deployment_metadata is None
            else deployment_metadata
        )

        if adapter:
            if not self.data.dynamic_adapter_loading_enabled:
                raise RuntimeError(f"Base deployment {self.name} is not configured to support LoRAX")

            # TODO: (magdy) check base model compatibility for hf based adapters here
            # (Delayed now since we need to do a roundtrip to hf) (INFRA-2052)
            # Directly import `Model` here to avoid cyclic import issues.
            from predibase.resource.model import Model

            if isinstance(adapter, Model) and self.data.model_name != adapter.llm_base_model_name:
                raise RuntimeError(
                    f"base deployment {self.name} does not match the adapter's base model. "
                    f"Expected base deployment model to be: {adapter.llm_base_model_name}. "
                    f"Actual: {self.data.model_name}",
                )

        self._adapter = adapter

    @property
    def adapter(self) -> Optional[Union["mdl.Model", HuggingFaceLLM]]:
        return self._adapter

    def with_adapter(self, model: Union["mdl.Model", HuggingFaceLLM]) -> "LLMDeployment":
        return LLMDeployment(
            session=self.session,
            name=self.name,
            adapter=model,
            deployment_metadata=self.data,
        )

    def generate(
        self,
        prompts: Union[str, List[str]],
        options: Optional[Dict[str, Union[str, float]]] = None,
    ) -> List[GeneratedResponse]:
        prompts = [prompts] if isinstance(prompts, str) else prompts

        resp_list, future_to_args = [], dict()
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for prompt in prompts:
                data = {
                    "inputs": prompt,
                    "parameters": options,
                }

                if self._adapter:
                    if isinstance(self._adapter, HuggingFaceLLM):
                        data["parameters"]["adapter_id"] = self._adapter.model_name
                        data["parameters"]["adapter_source"] = "hub"
                    else:
                        data["parameters"]["adapter_id"] = f"{self._adapter.repo.name}/{self._adapter.version}"
                        data["parameters"]["adapter_source"] = "s3"

                future = executor.submit(
                    self.session.post_json,
                    f"/llms/{self.name}/generate",
                    data,
                )
                future_to_args[future] = (self.name, prompt)
                futures.append(future)

            for future in concurrent.futures.as_completed(futures):
                try:
                    deployment_name, prompt = future_to_args[future]
                    res = future.result()
                    res = GeneratedResponse(
                        prompt=prompt,
                        response=res["generated_text"],
                        model_name=deployment_name,
                        generated_tokens=res["details"]["generated_tokens"],
                        prefill=res["details"]["prefill"],
                        tokens=res["details"]["tokens"],
                        finish_reason=res["details"]["finish_reason"],
                        seed=res["details"].get("seed"),  # optional
                        best_of_sequences=res["details"].get("best_of_sequences"),  # optional
                    )
                    resp_list.append(res)
                except Exception as exc:
                    print("ERROR:", exc)
        if len(resp_list) == 0:
            raise RuntimeError("LLM failed to generate a response. Please try again later.")
        return resp_list

    def prompt(
        self,
        data: Union[str, Dict[str, Any]],
        temperature: float = 0.1,
        max_new_tokens: int = 128,
        bypass_system_prompt: bool = False,
    ) -> GeneratedResponse:
        template = self.default_prompt_template
        if template is None:
            if isinstance(data, str):
                template = "{__pbase_data_input__}"
            elif len(data) == 1:
                template = f"{{{next(iter(data))}}}"
            else:
                raise RuntimeError(
                    "Unable to interpolate multiple keys in data into prompt " "- no default_prompt_template exists",
                )

        fields_in_template = {tpl[1] for tpl in Formatter().parse(template) if tpl[1] is not None}

        if isinstance(data, str):
            if len(fields_in_template) > 1:
                raise RuntimeError(
                    "Only a single string was provided as prompt input, but there are multiple "
                    "interpolation fields in the `default_prompt_template`.",
                )

            # Coerce data into a 1-element dict matching the single interpolation field
            # in the prompt template.
            data = {next(iter(fields_in_template)): data}

        used_keys = set()
        while fields_in_template:
            # We manually check for matching keys rather than using functions like
            # symmetric_difference() in order to account for defaultdict() and similar
            # constructions.
            fields_missing_in_data = [f for f in fields_in_template if f not in data]
            if fields_missing_in_data:
                raise RuntimeError(
                    f"The following fields were expected during prompt formatting but missing in the provided data: "
                    f"{','.join(fields_missing_in_data)}",
                )

            # Record data keys that have been used
            used_keys.update(fields_in_template)

            # Interpolate.
            # Double-escaping brackets is necessary to prevent errors during repeated parsing iterations.
            template = template.replace("{{", "{{{{").replace("}}", "}}}}")
            template = template.format_map(data)

            fields_in_template = {tpl[1] for tpl in Formatter().parse(template) if tpl[1] is not None}

        # Since we're preserving escaped brackets by double-escaping above, we need to do
        # one final replace in order to clean up the double-escapes.
        template = template.replace("{{", "{").replace("}}", "}")

        deployment_status = self.get_status()
        if deployment_status != "active":
            raise Exception(f"Target LLM deployment `{self.name}` is not active yet!")

        deployment_ready = self.is_ready()
        if not deployment_ready:
            print(f"WARNING: Target LLM deployment `{self.name}` is not fully scaled yet. Responses may be delayed...")

        # Check for fields provided in data that were never used in constructing the prompt.
        unused_keys = [f for f in data if f not in used_keys]
        if unused_keys:
            print(
                f"WARNING: The following fields were provided in the data but never used "
                f"when constructing the prompt: {','.join(unused_keys)}",
            )

        # Wrap with the system prompt template if one exists
        if self.data.prompt_template and not bypass_system_prompt:
            template = self.data.prompt_template % template

        # talk directly to the LLM, bypassing Temporal and the engines.
        responses = self.generate(
            template,
            options={"temperature": temperature, "max_new_tokens": max_new_tokens},
        )
        return responses[0]

    @functools.cached_property
    def default_prompt_template(self) -> Optional[str]:
        if self._adapter:
            # Dynamic adapter deployment case
            from predibase.resource.model import Model

            if isinstance(self._adapter, Model):
                adapter: Model = self._adapter
                return adapter.config.get("prompt", {}).get("template", None)
            else:
                # Some arbitrary HuggingFace adapter is being used.
                return None
        elif self.data.adapter_name:
            # Dedicated fine-tuned deployment case
            # Adapter name is actually the path to the model weights and has the form:
            # "<model_uuid>/<model_best_run_id>/artifacts/model/model_weights/"
            model_uuid = self.data.adapter_name.split("/")[0]
            try:
                resp = self.session.get_json(f"/models/version/uuid/{model_uuid}")
                model = build_model(resp, self.session)
                return model.config.get("prompt", {}).get("template", None)
            except Exception as e:
                raise RuntimeError("Failed to get info on registered adapter") from e
        else:
            # Base OSS LLM deployment case
            return None

    def delete(self):
        print(f"Requested deletion of llm deployment: `{self.name}` ...")
        endpoint = f"/llms/{self.name}"
        resp = self.session._delete(endpoint)
        if not resp.ok:
            raise RuntimeError(f"Failed to trigger LLM deletion - got status {resp.status_code} -- {resp.reason}")

        while True:
            try:
                llm_deployment = self.session.get_json(endpoint)
                if llm_deployment is None:
                    print(f"Successfully deleted llm deployment: `{self.name}`")
                    break
            except Exception as e:
                raise RuntimeError(f"Error while deleting deployment `{self.name}`: {e} {type(e)}")
            time.sleep(1.0)

    def is_ready(self) -> bool:
        resp = self.session.get_json(f"/llms/{self.name}/ready")
        return LLMDeploymentReadyResponse.from_dict(resp).ready

    def wait_for_ready(self, timeout_seconds: int = 600, poll_interval_seconds: int = 5) -> bool:
        start = time.time()
        while int(time.time() - start) < timeout_seconds:
            if self.is_ready():
                return True
            time.sleep(poll_interval_seconds)
        return False

    def is_scaled(self) -> bool:
        resp = self.session.get_json(f"/llms/{self.name}/scaled")
        return LLMDeploymentScaledResponse.from_dict(resp).scaled

    def get_status(self) -> str:
        resp = _LLMDeployment.from_dict(self.session.get_json(f"/llms/{self.name}"))
        return resp.deployment_status


class LLMDeploymentJob:
    def __init__(self, deployment_name: str, session: "Session"):
        self._deployment_name = deployment_name
        self._uri = f"pb://jobs/deploy::{deployment_name}"
        self._session = session

    def get(self) -> LLMDeployment:
        resp = self._session.get_llm_deployment_until_with_logging(
            f"/llms/{self._deployment_name}",
            lambda resp: resp["deploymentStatus"] == "active",
            lambda resp: f"Failed to create deployment {self._deployment_name} with status {resp['deploymentStatus']}"
            if resp["deploymentStatus"] in ("failed", "canceled")
            else None,
        )

        return LLMDeployment(self._session, self._deployment_name, deployment_metadata=_LLMDeployment.from_dict(resp))

    def cancel(self):
        return self._session.post_json(f"/llms/{self._deployment_name}/cancel", {})


def get_or_create_repo(session: "Session", repo_name: str) -> "mdl.ModelRepo":
    return mdl.create_model_repo(session, name=repo_name, exists_ok=True)
