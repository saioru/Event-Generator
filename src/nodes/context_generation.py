"""Context Generation Node Initialization"""
from pydantic import BaseModel, Field
from langchain_core.prompts.chat import ChatPromptTemplate

from src.state import State
from src.model import LLM

class OpeningHours(BaseModel):
    """Pydantic BaseModel Class for Opening Hours Formatting"""
    Mon: str = \
        Field(description="Service hours in the 2400 format")
    Tues: str = \
        Field(description="Service hours in the 2400 format")
    Weds: str = \
        Field(description="Service hours in the 2400 format")
    Thurs: str = \
        Field(description="Service hours in the 2400 format")
    Fri: str = \
        Field(description="Service hours in the 2400 format")
    Sat: str = \
        Field(description="Service hours in the 2400 format")
    Sun: str = \
        Field(description="Service hours in the 2400 format")

class Offers(BaseModel):
    """Pydantic BaseModel Class for Offers Formatting"""
    name: str = \
        Field(description="Name of the subjected offer or service")
    price: str = \
        Field(description="Estimated price of the subjected offer or service")

class ImageDetails(BaseModel):
    """Pydantic BaseModel Class for Image Details Formatting"""
    name: str = \
        Field(description="Name of the subjected image")
    url: str = \
        Field(description="URL links to webpages or platforms of the subject")
    caption: str = \
        Field(description="Narrative detailed advertising captions within 70 words")
    hashtags: str = \
        Field(description="Relevant and trendy hashtags for the subject")

class ContextTemplate(BaseModel):
    """Pydantic BaseModel Class for Context Formatting"""
    name: str = \
        Field(description="Name of the location")
    address: str = \
        Field(description="Physical address of the location or event")
    openinghr: OpeningHours = \
        Field(description="Opening hours of each day in the 2400 format")
    description: str = \
        Field(description="An engaging 350-400 character description of the location or event")
    offers: list[Offers] = \
        Field(description="Top items or services offered with estimated prices")
    contact_no: str = \
        Field(description="Contact number with the format starting with '+65'")
    images: list[ImageDetails] = \
        Field(description="Subjective images that correlate with context of the service or event")
    citations: list[str] = \
        Field(description="Source URLS of news or articles in list format to the service or event")

    def parse(self) -> dict:
        """Parse necessary formats"""
        self.openinghr = self.openinghr.model_dump(exclude_unset=True)
        self.offers = {offer.name: offer.price for offer in self.offers}
        self.images = {
            image.name: {
                'url': image.url,
                'caption': image.caption,
                'hashtags': image.hashtags
            } for image in self.images
        }
        return self

class ContextParser(BaseModel):
    """Custom Output Parser for Context Generation"""
    output: list[ContextTemplate] = Field(description="Max of 2 relevant context examples")

    def parse(self) -> list[dict]:
        """Parse necessary formats"""
        # Convert the list of output instances to a list of dictionaries
        self.output = [o.parse() for o in self.output]
        return [o.model_dump(exclude_unset=True) for o in self.output]

PROMPT = "As a tour and event guide, provide a list of relevant context.\nRequest: {intent}"

def context_generation(state: State) -> bool:
    """Context Generation Node to create context based on the given request.

    Args:
        state (State): Graph State passing between node calls.

    Returns:
        dict: Dictionary key-value update for State `output`.
    """
    _response = (
        ChatPromptTemplate.from_template(PROMPT)
        | LLM.with_structured_output(ContextParser)
    ).invoke({'intent': state['intent']})

    return {'output': _response.parse()}
