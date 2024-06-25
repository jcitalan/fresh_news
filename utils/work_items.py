from robocorp import workitems

from utils.payload import Payload


class WorkItemHandler:
    """
    A handler class for managing work items in Robocorp processes.

    This class provides methods to retrieve the current work item's payload
    and update the payload of a work item.
    """

    def __init__(self) -> None:
        """
        Initializes the WorkItemHandler instance.
        """
        self.wi = workitems

    def get_current_payload(self) -> Payload:
        """
        Retrieves the payload of the current work item.

        Returns:
            Payload: The payload of the current work item.

        Raises:
            ValueError: If no current work item or if the payload is None.
        """
        item = self.wi.inputs.current
        if item is None or item.payload is None:
            raise ValueError("No current work item found or payload is None")
        return Payload.from_dict(item.payload)

    def update_payload(self, new_payload: Payload) -> None:
        """
        Updates the payload of the current work item with a new payload.

        Args:
            new_payload (Payload): The new payload to update the current
            work item with.
        """
        # Update the payload
        self.wi.outputs.create(payload=new_payload.to_dict())
