class CourtFindBaseException(Exception):
    """Base exception for all CourtFind errors."""


class ModelNotTrainedError(CourtFindBaseException):
    """Raised when inference is attempted before model files exist."""


class InvalidPlayerQueryError(CourtFindBaseException):
    """Raised when a player query is malformed or missing required fields."""


class UnsupportedSportError(CourtFindBaseException):
    """Raised when an unsupported sport is requested."""


class NoCourtsFoundError(CourtFindBaseException):
    """Raised when A* search returns zero results."""


class PreprocessingError(CourtFindBaseException):
    """Raised during feature encoding or scaling failures."""


class DataGenerationError(CourtFindBaseException):
    """Raised when synthetic dataset generation fails."""
