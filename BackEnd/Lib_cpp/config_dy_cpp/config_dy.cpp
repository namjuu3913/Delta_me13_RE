#include <pybind11/pybind11.h>
#include <string>
#include <stdexcept> // std::runtime_error
#include "../ExternalResorces/json.hpp"

using nlohmann::json;
namespace py = pybind11;

class config_dy
{
public:
    // Default values are initialized with the member declarations below
    config_dy() {} 
    ~config_dy() = default;

    void set_LLMServer_all(const std::string& in)
    {
        try {
            json input = json::parse(in);

            if (input.contains("MODEL_PATH") && input["MODEL_PATH"].is_string())
                MODEL_PATH = input["MODEL_PATH"].get<std::string>();

            if (input.contains("CTX_SIZE") && input["CTX_SIZE"].is_number_integer())
                CTX_SIZE = input["CTX_SIZE"].get<int>();

            if (input.contains("NGL") && input["NGL"].is_number_integer())
                NGL = input["NGL"].get<int>();

            if (input.contains("ALIAS") && input["ALIAS"].is_string())
                ALIAS = input["ALIAS"].get<std::string>();

            if (input.contains("VERBOSE") && input["VERBOSE"].is_boolean())
                VERBOSE = input["VERBOSE"].get<bool>();

            if (input.contains("BATCH_SIZE") && input["BATCH_SIZE"].is_number_integer())
                BATCH_SIZE = input["BATCH_SIZE"].get<int>();

            if (input.contains("FLASH_ATTN") && input["FLASH_ATTN"].is_boolean())
                FLASH_ATTN = input["FLASH_ATTN"].get<bool>();

            if (input.contains("temperature") && (input["temperature"].is_number_float() || input["temperature"].is_number_integer()))
                temperature = input["temperature"].get<float>();

            if (input.contains("max_tokens") && input["max_tokens"].is_number_integer())
                max_tokens = input["max_tokens"].get<int>();

            flag_ready = true;
        }
        catch (const nlohmann::json::parse_error& e) {
            throw py::value_error(std::string("invalid json: ") + e.what());
        }
        catch (const nlohmann::json::type_error& e) {
            throw py::value_error(std::string("type error: ") + e.what());
        }
        catch (const std::exception& e) {
            throw py::value_error(std::string("error: An unexpected error occurred. Details: ") + e.what());
        }
    }

    bool is_ready() const { return is_valid(); }

    // Getters
    const std::string& get_model_path() const { return MODEL_PATH; }
    int get_ctx_size() const { return CTX_SIZE; }
    int get_ngl() const { return NGL; }
    const std::string& get_alias() const { return ALIAS; }
    bool is_verbose() const { return VERBOSE; }
    int get_batch_size() const { return BATCH_SIZE; }
    bool use_flash_attn() const { return FLASH_ATTN; }
    float get_temperature() const { return temperature; }
    int get_max_tokens() const { return max_tokens; }

    // Get whole data as a JSON string
    std::string get_json() const
    {
        if (!is_valid())
            throw std::runtime_error("error: config is not initialized properly.");

        json j;
        j["MODEL_PATH"] = MODEL_PATH;
        j["CTX_SIZE"] = CTX_SIZE;
        j["NGL"] = NGL;
        j["ALIAS"] = ALIAS;
        j["VERBOSE"] = VERBOSE;
        j["BATCH_SIZE"] = BATCH_SIZE;
        j["FLASH_ATTN"] = FLASH_ATTN;
        j["temperature"] = temperature;
        j["max_tokens"] = max_tokens;

        return j.dump(4); // 4 space indentation
    }

    // Helper to check if essential values have been set
    bool is_valid() const
    {
        if (!flag_ready) return false;

        // Check if required values are still in their initial (sentinel) state.
        return (MODEL_PATH != "" &&
                CTX_SIZE != UNINITIALIZED_INT &&
                NGL != UNINITIALIZED_INT &&
                // ALIAS can be empty, so it's excluded from this check or validated differently
                BATCH_SIZE != UNINITIALIZED_INT &&
                temperature != UNINITIALIZED_FLOAT &&
                max_tokens != UNINITIALIZED_INT);
    }

private:
    // Sentinel values to indicate an uninitialized state
    int UNINITIALIZED_INT = -100;
    float UNINITIALIZED_FLOAT = -100.0f;

    bool flag_ready = false;

    // Config for the LLM Server
    std::string MODEL_PATH = "";
    int CTX_SIZE = UNINITIALIZED_INT;
    int NGL = UNINITIALIZED_INT;
    std::string ALIAS = "";
    bool VERBOSE = true;
    int BATCH_SIZE = UNINITIALIZED_INT;
    bool FLASH_ATTN = true;

    // Config for a chat request
    float temperature = UNINITIALIZED_FLOAT;
    int max_tokens = UNINITIALIZED_INT;
};

// =================================================================
// Pybind11 binding code
// =================================================================
PYBIND11_MODULE(config_module, m) {
    py::class_<config_dy>(m, "ConfigDy")
        .def(py::init<>(), "Default constructor")
        .def("set_all_from_json", &config_dy::set_LLMServer_all, "Set all config values from a JSON string")
        .def("is_ready", &config_dy::is_ready, "Check if the config is ready and valid")
        .def("get_json", &config_dy::get_json, "Get all config values as a JSON string")

        // Method bindings for getters
        .def("get_model_path", &config_dy::get_model_path)
        .def("get_ctx_size", &config_dy::get_ctx_size)
        .def("get_ngl", &config_dy::get_ngl)
        .def("get_alias", &config_dy::get_alias)
        .def("is_verbose", &config_dy::is_verbose)
        .def("get_batch_size", &config_dy::get_batch_size)
        .def("use_flash_attn", &config_dy::use_flash_attn)
        .def("get_temperature", &config_dy::get_temperature)
        .def("get_max_tokens", &config_dy::get_max_tokens)

        // Pythonic read-only properties for direct access
        .def_property_readonly("model_path", &config_dy::get_model_path)
        .def_property_readonly("ctx_size", &config_dy::get_ctx_size)
        .def_property_readonly("ngl", &config_dy::get_ngl)
        .def_property_readonly("alias", &config_dy::get_alias)
        .def_property_readonly("verbose", &config_dy::is_verbose)
        .def_property_readonly("batch_size", &config_dy::get_batch_size)
        .def_property_readonly("flash_attn", &config_dy::use_flash_attn)
        .def_property_readonly("temperature", &config_dy::get_temperature)
        .def_property_readonly("max_tokens", &config_dy::get_max_tokens);
}