#include <pybind11/pybind11.h>
#include <string>
#include "../ExternalResorces/json.hpp"

using nlohmann::json;

class config_dy
{
public:

private:
    // model's path
    std::string model_path;
    
};