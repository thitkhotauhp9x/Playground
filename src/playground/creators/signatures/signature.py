from typing import Annotated

from pydantic import BaseModel, Field

from hat.playground.creators.signatures.app_field import AppField
from hat.playground.creators.signatures.input import Input
from hat.playground.creators.signatures.output import Output


class Signature(BaseModel):
    prompt: Annotated[str, Input(description=""), Field(description="")]
    instruction: Annotated[str, Output(description="")]

    @classmethod
    def get_content(cls) -> str:
        inputs: list[AppField] = []
        outputs: list[AppField] = []
        for field_name, field_annotated in cls.model_fields.items():
            app_field = AppField(
                name=field_name,
                annotation=field_annotated.annotation.__name__,
                description=field_annotated.description,
            )
            for item in field_annotated.metadata:
                if isinstance(item, Input):
                    inputs.append(app_field)
                elif isinstance(item, Output):
                    outputs.append(app_field)
                else:
                    raise TypeError(f"Unexpected type {type(item)}")

        content = "Your input fields are:\n"
        for index, item in enumerate(inputs):
            content += (
                f"{index + 1}. `{item.name}`({item.annotation}): {item.description}\n"
            )
        content += "Your output fields are:\n"
        for index, item in enumerate(outputs):
            content += (
                f"{index + 1}. `{item.name}`({item.annotation}): {item.description}\n"
            )
        return content


def main():
    print(Signature.get_content())


if __name__ == "__main__":
    main()
