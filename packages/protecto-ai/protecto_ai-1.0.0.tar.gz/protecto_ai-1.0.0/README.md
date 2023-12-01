# Protecto.AI Python API Library #

Intelligent Data Tokenization for Enhanced Privacy and Security

Protecto.AI employs a sophisticated approach to data tokenization, ensuring the intelligent handling of sensitive information. By leveraging this smart solution, you can unlock the full potential of your data while seamlessly upholding data privacy and security - all through the convenience of an API. 

* Website: Visit our [Protecto.Ai Website](https://www.protecto.ai/)
* Documentation:  Access our [Tokenization Packages documentation](https://help.protecto.ai/tokenization-packages/)
* For Bugs and Issues tracking:
   Email us at [help@protecto.ai](mailto:help@protecto.ai)

## Installation:

To install Protecto.AI library, use the following command:

```
pip install protecto_ai
```

## Usage Example:

### ProtectoVault

Our tokenization process encompasses four distinct and customer-friendly methods for masking data:

* [Mask with AutoDetect](#mask-with-autodetect)
* [Mask with a Specific Token](#mask-with-a-specific-token)
* [Mask with a Specific Token and Format](#mask-with-a-specific-token-and-format)
* [Mask JSON Format](#mask-json-format)

To unmask data:

* [Unmask a Token](#unmask-a-token)

For more comprehensive information about our product, kindly visit our [website](https://www.protecto.ai/).

### Code Example: 
Import the ProtectoVault class from the protecto_ai module
````
from protecto_ai import ProtectoVault

# Create an instance of ProtectoVault with your authentication token
obj = ProtectoVault("<auth_token>")

````

To obtain the auth token, please refer to the [Step-by-Step Guide to Obtain Your Auth Token](https://help.protecto.ai/tokenization-packages/data-tokenization/step-by-step-guide-to-obtain-your-auth-token).

### Mask with AutoDetect:

This method automatically identifies and masks personal/sensitive data within specific sentences,  leaving the rest of the data intact.

```
# Pass a list of sensitive information as input for the mask method
result = obj.mask(["George Washington is happy", "Mark lives in the U.S.A"])
# Print the masked result
print(result)
```
This will give you the masked result:

```
{ 
  "data": [ 
    { 
      "value": "George Washington is happy", 
      "token_value": "<PER>wRePE302Qx vUc7DruuWm</PER> is happy", 
      "individual_tokens": [ 
        { 
          "value": "George Washington", 
          "pii_type": "PERSON", 
          "token": "wRePE302Qx vUc7DruuWm", 
          "prefix": "<PER>", 
          "suffix": "</PER>" 
        } 
    ] 
    }, 
    { 
      "value": "Mark lives in the U.S.A", 
      "token_value": "<PER>7FHnu7Uo2O</PER> lives in the <ADDRESS>oQLxg3gisk.G2jPUYZHcv.bHIrJ0Mb7k</ADDRESS>", 
      "individual_tokens": [ 
        { 
          "value": "Mark", 
          "pii_type": "PERSON", 
          "token": "7FHnu7Uo2O", 
          "prefix": "<PER>", 
          "suffix": "</PER>" 
        }, 
        { 
          "value": "U.S.A", 
          "pii_type": "GPE", 
          "token": "oQLxg3gisk.G2jPUYZHcv.bHIrJ0Mb7k", 
          "prefix": "<ADDRESS>", 
          "suffix": "</ADDRESS>" 
        } 
      ] 
    } 
  ], 
  "success": true, 
  "error": { 
    "message": "" 
  } 
} 
```

For more details, check the [link](https://help.protecto.ai/tokenization-packages/protecto-tokenization/auto-detect-masking).
### Mask with a Specific Token:

This method allows you to mask input data according to default token types (Text token, Special Token, Numeric Token) specified.

```
# pass list of values as an input for the mask method.Provide default token type.
result = obj.mask(["Mark","Australia"], "Text Token")
# Print the masked result
print(result)
```
You can get list of default token types in this [link](https://help.protecto.ai/tokenization-packages/data-tokenization/supporting-token-and-format-types).

Result:
```
{ 
  "data": [ 
    { 
      "value": "Australia", 
      "token_value": "1AN9X4Doab", 
      "token_name": "Text Token" 
    }, 
    { 
      "value": "Mark", 
      "token_value": "7FHnu7Uo2O", 
      "token_name": "Text Token" 
    } 
  ], 
  "success": true, 
  "error": { 
    "message": "" 
  } 

```
For more details, check the [link](https://help.protecto.ai/tokenization-packages/protecto-tokenization/masking-data-with-default-token-types).

### Mask with a Specific Token and Format:

This method allows you to mask input data according to default token types (Text token, Special Token, Numeric Token) and formats specified.
```
# pass list of sensitive information as an input for the mask method. Provide default token type and format
result = obj.mask(["(555) 123-4567"], "Numeric Token", "Phone Number")
# Print the masked result
print(result)
```
You can get the list of default token types and formats in this [link](https://help.protecto.ai/tokenization-packages/data-tokenization/supporting-token-and-format-types).

Result:
```
{ 
  "data": [ 
    { 
      "value": "(555) 123-4567", 
      "token_value": "(191004182137) 354826618175-127882693655", 
      "token_name": "Numeric Token", 
      "format": "Phone Number" 
    } 
  ], 
  "success": true, 
  "error": { 
    "message": "" 
  } 
} 
```
For more details, check the [link](https://help.protecto.ai/tokenization-packages/protecto-tokenization/masking-data-with-format-and-token-types).

### Mask JSON Format:


```
# pass list of sensitive information as an input in the provided JSON Format for the mask method
result = obj.mask({"mask": [{"value": "Ross", "token_name": "Text Token", "format": "Person Name"}]})
# Print the masked result
print(result)
```
Result:

```
{ 
  "data": [ 
    { 
      "value": "Ross", 
      "token_value": "EZN792djTe", 
      "token_name": "Text Token", 
      "format": "Person Name" 
    } 
  ], 
  "success": true, 
  "error": { 
    "message": "" 
  } 
} 
```
For more details, check the [link](https://help.protecto.ai/tokenization-packages/protecto-tokenization/mask-data-in-json-format).


### Unmask a Token:
This method allows you to retrieve the original data .

Let's take an example. If "George Williams" is masked as "wRePE302Qx vUc7DruuWm," and the user provides the second masked input, "vUc7DruuWm," the unmasked output would be "Williams."


```
result = obj.unmask(["<PER>wRePE302Qx vUc7DruuWm</PER> is happy","wRePE302Qx vUc7DruuWm","vUc7DruuWm"])
# Print the unmasked result
print(result)
```
Result:
```
{
  "data": [
    {
      "token_value": "<PER>wRePE302Qx vUc7DruuWm</PER> is happy",
      "value": "George Washington is happy"
    },
    {
      "token_value": "wRePE302Qx vUc7DruuWm",
      "value": "George Washington"
    },
    {
      "token_value": "vUc7DruuWm",
      "value": "Washington"
    }
  ],
  "success": true,
  "error": {
    "message": ""
  }
}
```
For more details, check the [link](https://help.protecto.ai/tokenization-packages/protecto-tokenization/unmasking-the-token).
