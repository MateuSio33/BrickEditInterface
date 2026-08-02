from dataclasses import dataclass


@dataclass
class TooltipContents:
    text: str
    description: str | None = None

    def richtext(self):
        if self.description is None or self.description == "":
            return self.text

        description_br = self.description.replace('\n', '<br>')
        return f"<b>{self.text}</b><br><br>{description_br}"
