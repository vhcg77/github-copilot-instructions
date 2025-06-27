---
title: "QA Enhanced Test Generation"
description: "Generate comprehensive test suites using MCP tools for enhanced context"
applyTo: ["testing", "validation", "quality-assurance"]
mode: "agent"
tools: ["context7", "consult7", "duckduckgo", "github", "pytest"]
role: "qa-engineer"
priority: "high"
---

# QA Enhanced Test Generation

## Objective
Generate comprehensive, production-ready test suites leveraging MCP tools for enhanced context and current best practices.

## Enhanced Testing Workflow

### Phase 1: Research and Context Gathering
```
1. Context7 Research:
   "pytest fixtures and parametrization patterns, use context7"
   "Great Expectations data validation patterns, use context7"

2. Existing Code Analysis:
   Use Consult7 to analyze current test patterns in /tests/ directory
   Identify testing gaps and coverage opportunities

3. Best Practices Research:
   Use DuckDuckGo: "Python data validation testing strategies 2025"
   Use DuckDuckGo: "pytest performance testing patterns"

4. Reference Implementations:
   Use GitHub Tools: Find comprehensive test suites in data science projects
   Analyze testing patterns for similar business domains
```

### Phase 2: Test Generation with Enhanced Context

## Example MCP-Enhanced Test Generation Request

```
"Generate comprehensive test suite for inventory validation module that:

1. Tests data quality checks for product_id, quantity, and location fields
2. Validates business rules for inventory thresholds  
3. Tests API endpoints for inventory CRUD operations
4. Includes performance tests for large datasets
5. Uses proper fixtures and parametrization

Enhanced Research:
- use context7 for pytest and pandera latest patterns
- Use consult7 to analyze existing test patterns in /tests/
- Search with duckduckgo: 'inventory management testing best practices 2025'
- Find reference implementations in GitHub for similar data validation tests"
```

## Expected Output Structure

### 1. Test Configuration and Fixtures
```python
import pytest
import pandas as pd
import numpy as np
from typing import List, Dict, Any
from unittest.mock import Mock, patch
import requests

from src.data.validation import InventoryValidator
from src.api.inventory import InventoryAPI

@pytest.fixture
def sample_inventory_data() -> pd.DataFrame:
    """Sample inventory data for testing."""
    return pd.DataFrame({
        'product_id': ['GS0001', 'GS0002', 'GS0003'],
        'quantity': [100, 50, 200],
        'location': ['WAREHOUSE_A', 'WAREHOUSE_B', 'STORE_01'],
        'updated_at': pd.to_datetime(['2025-01-01', '2025-01-02', '2025-01-03'])
    })

@pytest.fixture
def invalid_inventory_data() -> pd.DataFrame:
    """Invalid inventory data for edge case testing."""
    return pd.DataFrame({
        'product_id': ['INVALID', '', None],
        'quantity': [-10, None, 999999],
        'location': ['INVALID_LOC', None, ''],
        'updated_at': [None, 'invalid-date', '2025-01-01']
    })
```

### 2. Data Quality Tests
```python
class TestInventoryDataQuality:
    """Test suite for inventory data quality validation."""
    
    def test_valid_product_id_format(self, sample_inventory_data):
        """Test that valid product IDs pass validation."""
        validator = InventoryValidator()
        result = validator.validate_product_ids(sample_inventory_data)
        assert result.is_valid
        assert len(result.errors) == 0
    
    @pytest.mark.parametrize("invalid_id", [
        "invalid-format",
        "",
        None,
        "TOO_LONG_ID_12345",
        "123456"  # numeric only
    ])
    def test_invalid_product_id_format(self, invalid_id):
        """Test that invalid product IDs are rejected."""
        test_data = pd.DataFrame({'product_id': [invalid_id]})
        validator = InventoryValidator()
        result = validator.validate_product_ids(test_data)
        assert not result.is_valid
        assert len(result.errors) > 0
```

### 3. API Integration Tests
```python
class TestInventoryAPI:
    """Test suite for inventory API endpoints."""
    
    @pytest.fixture
    def api_client(self):
        """Mock API client for testing."""
        return InventoryAPI(base_url="http://test-api.local")
    
    def test_get_inventory_success(self, api_client, sample_inventory_data):
        """Test successful inventory retrieval."""
        with patch.object(requests, 'get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                'items': sample_inventory_data.to_dict('records'),
                'total_count': len(sample_inventory_data)
            }
            mock_get.return_value = mock_response
            
            result = api_client.get_inventory()
            
            assert result.success
            assert len(result.items) == 3
            assert result.total_count == 3
```

### 4. Performance Tests
```python
class TestInventoryPerformance:
    """Performance tests for inventory operations."""
    
    @pytest.mark.performance
    def test_large_dataset_processing_performance(self):
        """Test processing performance with large datasets."""
        # Generate large test dataset
        large_data = self._generate_large_inventory_dataset(100000)
        
        start_time = time.time()
        validator = InventoryValidator()
        result = validator.validate_full_dataset(large_data)
        end_time = time.time()
        
        processing_time = end_time - start_time
        
        # Performance requirements: 100k records in < 30 seconds
        assert processing_time < 30.0, f"Processing took {processing_time:.2f}s"
        assert result.is_valid
        
    def _generate_large_inventory_dataset(self, size: int) -> pd.DataFrame:
        """Generate large dataset for performance testing."""
        np.random.seed(42)
        return pd.DataFrame({
            'product_id': [f'GS{i:04d}' for i in range(size)],
            'quantity': np.random.randint(1, 1000, size),
            'location': np.random.choice(['WAREHOUSE_A', 'WAREHOUSE_B', 'STORE_01'], size)
        })
```

## Quality Validation Checklist

### ✅ Test Coverage Requirements
- [ ] Happy path scenarios covered
- [ ] Edge cases and boundary conditions tested
- [ ] Error handling and exception scenarios
- [ ] Performance requirements validated
- [ ] Integration points tested
- [ ] Business rule validation complete

### ✅ Code Quality Standards
- [ ] Type hints for all test functions
- [ ] Descriptive test names and docstrings
- [ ] Proper use of fixtures and parametrization
- [ ] Mock objects for external dependencies
- [ ] Clear arrange-act-assert structure

### ✅ MCP Tool Integration Verification
- [ ] Context7 provided current testing framework patterns
- [ ] Consult7 analyzed existing test structure for consistency
- [ ] DuckDuckGo research informed testing strategy
- [ ] GitHub references provided implementation examples

## Usage Instructions

1. **Activate MCP Research**: Always start test generation with MCP tool research phase
2. **Analyze Existing Patterns**: Use Consult7 to understand current test organization
3. **Follow Current Practices**: Ensure generated tests align with project standards
4. **Validate Implementation**: Run generated tests to verify they work correctly

## Example Command
```bash
# Run specific test classes
pytest tests/test_inventory_validation.py::TestInventoryDataQuality -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run performance tests only
pytest tests/ -m performance
```

---

**Note**: This prompt demonstrates how MCP tools enhance test generation by providing current best practices, analyzing existing patterns, and ensuring comprehensive coverage based on real-world implementations.
