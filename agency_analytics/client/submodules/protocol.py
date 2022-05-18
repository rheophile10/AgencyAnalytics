from typing import Protocol, List, Any

class ClientModule(Protocol):
    """A very general protocol for the client"""

    def data(self, **kwargs) -> List[Any]:
        """returns agency analytics data"""
        raise NotImplementedError