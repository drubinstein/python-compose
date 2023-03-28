from abc import ABC, abstractmethod


class ComposeUnit(ABC):
    """An abstract base class representing the base for a Python Compose Unit."""

    @abstractmethod
    def create(self) -> None:
        """Function for creating a virtual environment."""
        raise NotImplementedError("This is an abstract method!")

    @abstractmethod
    def install_requirements(self) -> None:
        """Function to install any and all requirements for running a script in the virtual
        environment."""
        raise NotImplementedError("This is an abstract method!")

    @abstractmethod
    def start(self) -> None:
        """Function to start a script in the previously created virtual environment."""
        raise NotImplementedError("This is an abstract method!")

    @abstractmethod
    def clean(self) -> None:
        """Function to erase any pre-existing files to be recreated by a Python Compose Unit."""
        raise NotImplementedError("This is an abstract method!")
