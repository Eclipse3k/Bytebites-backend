from enum import Enum

class Feature(Enum):
    """Enum for feature flags."""
    NUTRITION_TRACKING = "nutrition_tracking"

class FeatureFlags:
    """Class to manage feature flags."""
    _enabled_features = set()

    @classmethod
    def enable(cls, feature: Feature):
        """Enable a feature flag."""
        cls._enabled_features.add(feature)

    @classmethod
    def disable(cls, feature: Feature):
        """Disable a feature flag."""
        cls._enabled_features.discard(feature)

    @classmethod
    def is_enabled(cls, feature: Feature) -> bool:
        """Check if a feature is enabled."""
        return feature in cls._enabled_features

    @classmethod
    def reset(cls):
        """Reset all feature flags to disabled state."""
        cls._enabled_features.clear()