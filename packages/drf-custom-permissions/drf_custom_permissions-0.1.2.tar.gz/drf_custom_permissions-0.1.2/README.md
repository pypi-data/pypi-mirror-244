# drf-permissions

## Installation

```pip
pip install drf-custom-permissions
```

## Usage

### APIView IsNotAuthenticated permission

```python
# views.py

from rest_framework.views import APIView
from drf_custom_permissions import IsNotAuthenticated

class ExampleIsNotAuthenticatedAPIVIew(APIView):
    permission_classes = (IsNotAuthenticated,)
    ...
```

### APIView with HasGroupPermission

```python
# views.py

from rest_framework.views import APIView
from drf_custom_permissions import HasGroupPermission

class ExampleIsNotAuthenticatedAPIVIew(APIView):
    permission_classes = (HasGroupPermission,)
    permission_groups = ('Designers', 'Developers',)
    ...
```