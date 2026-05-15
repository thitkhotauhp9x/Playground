from pydantic import BaseModel

from hat.instructions.base_instruction import BaseInstruction
from hat.instructions.check_identity import check_identity


class SystemTemplate(BaseModel):
    identity: str
    instructions: list[BaseInstruction]

    def _check_identity(self):
        result = check_identity(self.identity)
        assert result == True
