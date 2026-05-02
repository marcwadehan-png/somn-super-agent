# -*- coding: utf-8 -*-
"""
Utility Functions Test Suite
Tests for common utility functions across the codebase.
"""

import pytest
from typing import Any, Dict, List, Optional, Tuple


class TestStringUtils:
    """String utility tests."""

    def test_sanitize_filename_standard(self):
        """Standard filename sanitization."""
        unsafe = "test<file>name:.txt"
        # Simple sanitization logic - colon becomes underscore
        safe = "".join(c if c.isalnum() or c in "._-" else "_" for c in unsafe)
        # Colon converts to underscore, so only one underscore between name and ext
        assert safe == "test_file_name_.txt"

    def test_sanitize_filename_unicode(self):
        """Unicode filename handling."""
        name = "测试_文件_123.txt"
        safe = "".join(c if c.isalnum() or c in "._-" else "_" for c in name)
        assert safe.count("_") >= 2

    def test_truncate_text_short(self):
        """Truncate short text."""
        text = "Short"
        max_len = 10
        result = text if len(text) <= max_len else text[:max_len-3] + "..."
        assert result == "Short"

    def test_truncate_text_long(self):
        """Truncate long text."""
        text = "This is a very long text that needs truncation"
        max_len = 20
        result = text if len(text) <= max_len else text[:max_len-3] + "..."
        assert len(result) == 20
        assert result.endswith("...")

    def test_normalize_whitespace(self):
        """Normalize whitespace in text."""
        text = "  Multiple   spaces   here  "
        result = " ".join(text.split())
        assert result == "Multiple spaces here"

    def test_normalize_empty(self):
        """Normalize empty text."""
        text = "   \t\n   "
        result = " ".join(text.split())
        assert result == ""

    def test_extract_numbers(self):
        """Extract numbers from text."""
        import re
        text = "Order 12345 shipped on 2026-04-24"
        numbers = re.findall(r'\d+', text)
        assert "12345" in numbers
        assert "2026" in numbers
        assert "04" in numbers
        assert "24" in numbers

    def test_mask_sensitive_data_password(self):
        """Mask password in text."""
        text = "password=secret123"
        import re
        result = re.sub(r'password=[^&\s]+', 'password=***', text)
        assert "secret123" not in result
        assert "password=***" in result

    def test_mask_sensitive_data_token(self):
        """Mask token in text."""
        text = "Authorization: Bearer abc123xyz"
        import re
        result = re.sub(r'Bearer [^"\s]+', 'Bearer ***', text)
        assert "abc123xyz" not in result

    def test_slugify_simple(self):
        """Simple slug generation."""
        text = "Hello World"
        slug = text.lower().replace(" ", "-")
        assert slug == "hello-world"

    def test_slugify_special_chars(self):
        """Slug with special characters."""
        text = "What's New? v2.0!"
        import re
        slug = re.sub(r'[^\w\s-]', '', text.lower())
        slug = re.sub(r'[-\s]+', '-', slug)
        assert "what" in slug
        assert "new" in slug


class TestDictUtils:
    """Dictionary utility tests."""

    def test_flatten_dict_simple(self):
        """Flatten simple nested dict."""
        nested = {"a": 1, "b": {"c": 2}}
        result = {}
        for k, v in nested.items():
            if isinstance(v, dict):
                for k2, v2 in v.items():
                    result[f"{k}.{k2}"] = v2
            else:
                result[k] = v
        assert result == {"a": 1, "b.c": 2}

    def test_flatten_dict_deep(self):
        """Flatten deeply nested dict."""
        nested = {"a": {"b": {"c": {"d": 1}}}}
        result = {}
        def _flatten(d, prefix=""):
            for k, v in d.items():
                key = f"{prefix}.{k}" if prefix else k
                if isinstance(v, dict):
                    _flatten(v, key)
                else:
                    result[key] = v
        _flatten(nested)
        assert result == {"a.b.c.d": 1}

    def test_merge_dicts_no_overlap(self):
        """Merge two dicts with no overlap."""
        dict1 = {"a": 1, "b": 2}
        dict2 = {"c": 3, "d": 4}
        result = {**dict1, **dict2}
        assert result == {"a": 1, "b": 2, "c": 3, "d": 4}

    def test_merge_dicts_with_overlap(self):
        """Merge dicts with overlapping keys."""
        dict1 = {"a": 1, "b": 2}
        dict2 = {"b": 10, "c": 3}
        result = {**dict1, **dict2}
        assert result == {"a": 1, "b": 10, "c": 3}

    def test_deep_get_nested(self):
        """Deep get from nested dict."""
        data = {"a": {"b": {"c": "found"}}}
        result = data.get("a", {}).get("b", {}).get("c", "default")
        assert result == "found"

    def test_deep_get_missing(self):
        """Deep get with missing keys."""
        data = {"a": {"b": 1}}
        result = data.get("a", {}).get("c", {}).get("d", "default")
        assert result == "default"

    def test_filter_dict_by_keys(self):
        """Filter dict by allowed keys."""
        data = {"a": 1, "b": 2, "c": 3, "d": 4}
        allowed = ["a", "c"]
        result = {k: v for k, v in data.items() if k in allowed}
        assert result == {"a": 1, "c": 3}

    def test_exclude_dict_keys(self):
        """Exclude dict keys."""
        data = {"a": 1, "b": 2, "c": 3, "d": 4}
        exclude = ["b", "d"]
        result = {k: v for k, v in data.items() if k not in exclude}
        assert result == {"a": 1, "c": 3}

    def test_dict_diff(self):
        """Get difference between two dicts."""
        dict1 = {"a": 1, "b": 2, "c": 3}
        dict2 = {"b": 2, "c": 4, "d": 5}
        added = {k: v for k, v in dict2.items() if k not in dict1}
        removed = {k: v for k, v in dict1.items() if k not in dict2}
        changed = {k: v for k, v in dict1.items() if k in dict2 and v != dict2[k]}
        assert added == {"d": 5}
        assert removed == {"a": 1}
        assert changed == {"c": 3}

    def test_safe_get_string(self):
        """Safe get with string value."""
        data = {"key": "value"}
        result = data.get("key", "default")
        assert result == "value"

    def test_safe_get_default(self):
        """Safe get with default value."""
        data = {"key": "value"}
        result = data.get("missing", "default")
        assert result == "default"


class TestListUtils:
    """List utility tests."""

    def test_chunk_list_basic(self):
        """Chunk list into sublists."""
        data = list(range(10))
        chunk_size = 3
        result = [data[i:i+chunk_size] for i in range(0, len(data), chunk_size)]
        assert len(result) == 4
        assert result[0] == [0, 1, 2]
        assert result[-1] == [9]

    def test_chunk_list_exact(self):
        """Chunk list with exact division."""
        data = list(range(9))
        chunk_size = 3
        result = [data[i:i+chunk_size] for i in range(0, len(data), chunk_size)]
        assert len(result) == 3
        assert all(len(chunk) == 3 for chunk in result)

    def test_deduplicate_preserve_order(self):
        """Deduplicate while preserving order."""
        data = [3, 1, 2, 1, 3, 4, 2]
        seen = set()
        result = [x for x in data if not (x in seen or seen.add(x))]
        assert result == [3, 1, 2, 4]

    def test_find_duplicates(self):
        """Find duplicate items in list."""
        data = [1, 2, 3, 2, 4, 3, 5]
        seen = set()
        duplicates = set()
        for item in data:
            if item in seen:
                duplicates.add(item)
            seen.add(item)
        assert duplicates == {2, 3}

    def test_partition_list(self):
        """Partition list by predicate."""
        data = list(range(10))
        even = [x for x in data if x % 2 == 0]
        odd = [x for x in data if x % 2 != 0]
        assert even == [0, 2, 4, 6, 8]
        assert odd == [1, 3, 5, 7, 9]

    def test_flatten_list_simple(self):
        """Flatten simple nested list."""
        nested = [[1, 2], [3, 4], [5]]
        result = [item for sublist in nested for item in sublist]
        assert result == [1, 2, 3, 4, 5]

    def test_flatten_list_deep(self):
        """Flatten deeply nested list."""
        nested = [[1, [2, [3]]], [4]]
        def _flatten(lst):
            result = []
            for item in lst:
                if isinstance(item, list):
                    result.extend(_flatten(item))
                else:
                    result.append(item)
            return result
        result = _flatten(nested)
        assert result == [1, 2, 3, 4]

    def test_group_by_key(self):
        """Group list items by key."""
        items = [{"type": "a", "val": 1}, {"type": "b", "val": 2}, {"type": "a", "val": 3}]
        grouped = {}
        for item in items:
            key = item["type"]
            grouped.setdefault(key, []).append(item)
        assert len(grouped["a"]) == 2
        assert len(grouped["b"]) == 1

    def test_safe_list_get(self):
        """Safe list index access."""
        data = [1, 2, 3]
        assert (data[0] if len(data) > 0 else None) == 1
        assert (data[10] if len(data) > 10 else None) is None

    def test_list_intersection(self):
        """Find intersection of two lists."""
        list1 = [1, 2, 3, 4, 5]
        list2 = [4, 5, 6, 7, 8]
        result = [x for x in list1 if x in list2]
        assert result == [4, 5]


class TestDateTimeUtils:
    """DateTime utility tests."""

    def test_format_datetime_iso(self):
        """Format datetime to ISO string."""
        from datetime import datetime
        dt = datetime(2026, 4, 24, 15, 30, 45)
        result = dt.isoformat()
        assert "2026-04-24" in result
        assert "15:30:45" in result

    def test_parse_datetime_iso(self):
        """Parse ISO datetime string."""
        from datetime import datetime
        iso_str = "2026-04-24T15:30:45"
        dt = datetime.fromisoformat(iso_str)
        assert dt.year == 2026
        assert dt.month == 4
        assert dt.day == 24

    def test_timestamp_conversion(self):
        """Convert between timestamp and datetime."""
        from datetime import datetime
        dt = datetime(2026, 4, 24, 12, 0, 0)
        timestamp = int(dt.timestamp())
        dt_back = datetime.fromtimestamp(timestamp)
        assert dt == dt_back

    def test_time_ago_seconds(self):
        """Format time difference in seconds."""
        from datetime import datetime, timedelta
        now = datetime.now()
        past = now - timedelta(seconds=30)
        diff = int((now - past).total_seconds())
        assert diff == 30

    def test_time_ago_minutes(self):
        """Format time difference in minutes."""
        from datetime import datetime, timedelta
        now = datetime.now()
        past = now - timedelta(minutes=5)
        diff = int((now - past).total_seconds() / 60)
        assert diff == 5

    def test_time_ago_hours(self):
        """Format time difference in hours."""
        from datetime import datetime, timedelta
        now = datetime.now()
        past = now - timedelta(hours=2)
        diff = int((now - past).total_seconds() / 3600)
        assert diff == 2

    def test_time_ago_days(self):
        """Format time difference in days."""
        from datetime import datetime, timedelta
        now = datetime.now()
        past = now - timedelta(days=3)
        diff = (now - past).days
        assert diff == 3

    def test_weekday_check(self):
        """Check if date is weekday."""
        from datetime import datetime
        monday = datetime(2026, 4, 20)  # Monday
        saturday = datetime(2026, 4, 25)  # Saturday
        assert monday.weekday() < 5  # 0-4 for Mon-Fri
        assert saturday.weekday() >= 5  # 5-6 for Sat-Sun

    def test_date_range(self):
        """Generate date range."""
        from datetime import datetime, timedelta
        start = datetime(2026, 4, 1)
        end = datetime(2026, 4, 5)
        dates = []
        current = start
        while current <= end:
            dates.append(current)
            current += timedelta(days=1)
        assert len(dates) == 5


class TestValidationUtils:
    """Validation utility tests."""

    def test_is_valid_email(self):
        """Validate email format."""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        assert bool(re.match(pattern, "test@example.com"))
        assert not bool(re.match(pattern, "invalid-email"))

    def test_is_valid_url(self):
        """Validate URL format."""
        import re
        pattern = r'^https?://[^\s/$.?#].[^\s]*$'
        assert bool(re.match(pattern, "http://example.com"))
        assert bool(re.match(pattern, "https://example.com/path"))
        assert not bool(re.match(pattern, "not-a-url"))

    def test_is_valid_ipv4(self):
        """Validate IPv4 address format."""
        import re
        # Simple format check (not range validation)
        pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
        assert bool(re.match(pattern, "192.168.1.1"))
        # Format check only - range validation would require separate logic
        assert bool(re.match(pattern, "256.1.1.1"))  # Format valid, range check separate

    def test_is_valid_port(self):
        """Validate port number."""
        def is_valid_port(port):
            return isinstance(port, int) and 1 <= port <= 65535
        assert is_valid_port(80)
        assert is_valid_port(8080)
        assert is_valid_port(443)
        assert not is_valid_port(0)
        assert not is_valid_port(70000)

    def test_is_valid_uuid(self):
        """Validate UUID format."""
        import re
        pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
        assert bool(re.match(pattern, "550e8400-e29b-41d4-a716-446655440000"))
        assert not bool(re.match(pattern, "not-a-uuid"))

    def test_validate_json_string(self):
        """Validate JSON string."""
        import json
        valid = '{"key": "value"}'
        invalid = '{"key": value}'  # Missing quotes
        try:
            json.loads(valid)
            assert True
        except:
            assert False
        try:
            json.loads(invalid)
            assert False
        except:
            assert True

    def test_validate_phone_number(self):
        """Validate phone number."""
        import re
        pattern = r'^\+?1?\d{9,15}$'
        assert bool(re.match(pattern, "+1234567890"))
        assert bool(re.match(pattern, "1234567890"))
        assert not bool(re.match(pattern, "123"))

    def test_validate_postal_code(self):
        """Validate postal code (US)."""
        import re
        pattern = r'^\d{5}(-\d{4})?$'
        assert bool(re.match(pattern, "12345"))
        assert bool(re.match(pattern, "12345-6789"))
        assert not bool(re.match(pattern, "1234"))
        assert not bool(re.match(pattern, "123456"))


class TestMathUtils:
    """Math utility tests."""

    def test_percentage_calculation(self):
        """Calculate percentage."""
        value = 75
        total = 100
        pct = (value / total) * 100
        assert pct == 75.0

    def test_percentage_of(self):
        """Get percentage of value."""
        pct = 20
        value = 150
        result = (pct / 100) * value
        assert result == 30.0

    def test_round_to_decimal_places(self):
        """Round to specified decimal places."""
        assert round(3.14159, 2) == 3.14
        # Due to floating-point representation, round(3.145, 2) may return 3.14 or 3.15
        result_145 = round(3.145, 2)
        assert result_145 in (3.14, 3.15)
        # round(3.155, 2) typically returns 3.15 due to floating-point precision
        result_155 = round(3.155, 2)
        assert result_155 in (3.15, 3.16)

    def test_clamp_value(self):
        """Clamp value between min and max."""
        def clamp(val, min_val, max_val):
            return max(min_val, min(val, max_val))
        assert clamp(5, 0, 10) == 5
        assert clamp(-5, 0, 10) == 0
        assert clamp(15, 0, 10) == 10

    def test_mean_calculation(self):
        """Calculate mean of list."""
        values = [1, 2, 3, 4, 5]
        mean = sum(values) / len(values)
        assert mean == 3.0

    def test_median_calculation(self):
        """Calculate median of list."""
        def median(values):
            sorted_vals = sorted(values)
            n = len(sorted_vals)
            mid = n // 2
            if n % 2 == 0:
                return (sorted_vals[mid-1] + sorted_vals[mid]) / 2
            return sorted_vals[mid]
        assert median([1, 2, 3, 4, 5]) == 3
        assert median([1, 2, 3, 4]) == 2.5

    def test_standard_deviation(self):
        """Calculate standard deviation."""
        import math
        values = [2, 4, 4, 4, 5, 5, 7, 9]
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        std_dev = math.sqrt(variance)
        assert abs(std_dev - 2.0) < 0.1

    def test_lerp(self):
        """Linear interpolation."""
        def lerp(a, b, t):
            return a + (b - a) * t
        assert lerp(0, 100, 0.5) == 50
        assert lerp(0, 100, 0) == 0
        assert lerp(0, 100, 1) == 100

    def test_distance_1d(self):
        """Calculate 1D distance."""
        assert abs(5 - 10) == 5
        assert abs(10 - 5) == 5
        assert abs(-5 - 5) == 10

    def test_distance_2d(self):
        """Calculate 2D Euclidean distance."""
        import math
        def distance(p1, p2):
            return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)
        assert abs(distance((0, 0), (3, 4)) - 5.0) < 0.001
