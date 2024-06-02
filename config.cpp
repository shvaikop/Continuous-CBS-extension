#include "config.h"
#include "logger_macros.h"


using namespace  tinyxml2;
Config::Config()
{
    connectdness = CN_CONNECTEDNESS;
    use_cardinal = CN_USE_CARDINAL;
    agent_size = CN_AGENT_SIZE;
    timelimit = CN_TIMELIMIT;
    focal_weight = CN_FOCAL_WEIGHT;
    precision = CN_PRECISION;
}


void Config::getConfig(const char *fileName)
{
    std::stringstream stream;
    XMLDocument doc;
    if (doc.LoadFile(fileName) != tinyxml2::XMLError::XML_SUCCESS)
    {
        LOG_ERROR("Error opening Config XML file");
        return;
    }

    XMLElement *root = doc.FirstChildElement(CNS_TAG_ROOT);
    if (!root)
    {
        LOG_ERROR("No 'root' element found in XML file.");
        return;
    }

    XMLElement *algorithm = root->FirstChildElement(CNS_TAG_ALGORITHM);
    if(!algorithm)
    {
        LOG_ERROR("No 'algorithm' element found in XML file.");
        return;
    }

    XMLElement *element = algorithm->FirstChildElement("precision");
    if (!element)
    {
        LOG_WARNING("Error! No 'precision' element found inside '{}' section. It's compared to '{}'.", CNS_TAG_ALGORITHM, CN_PRECISION);
        precision = CN_PRECISION;
    }
    else
    {
        auto value = element->GetText();
        stream<<value;
        stream>>precision;
        if(precision > 1.0 || precision <= 0)
        {
            LOG_WARNING("Error! Wrong 'precision' element found inside '{}' section. It's compared to '{}'.", CNS_TAG_ALGORITHM, CN_PRECISION);
            precision = CN_PRECISION;
        }
        stream.clear();
        stream.str("");
    }

    element = algorithm->FirstChildElement("use_cardinal");
    if (!element)
    {
        LOG_WARNING("Error! No 'use_cardinal' element found inside '{}' section. It's compared to '{}'.", CNS_TAG_ALGORITHM, CN_USE_CARDINAL);
        use_cardinal = CN_USE_CARDINAL;
    }
    else
    {
        std::string value = element->GetText();
        if(value.compare("true") == 0 || value.compare("1") == 0)
        {
            use_cardinal = true;
        }
        else if(value.compare("false") == 0 || value.compare("0") == 0)
        {
            use_cardinal = false;
        }
        else
        {
            std::cout << "Error! Wrong 'use_cardinal' value found inside '"<<CNS_TAG_ALGORITHM<<"' section. It's compared to '"<<CN_USE_CARDINAL<<"'."<<std::endl;
            use_cardinal = CN_USE_CARDINAL;
        }
    }

    element = algorithm->FirstChildElement("use_disjoint_splitting");
    if (!element)
    {
        LOG_WARNING("Error! No 'use_disjoint_splitting' element found inside '{}' section. It's compared to '{}'.", CNS_TAG_ALGORITHM, CN_USE_DS);
        use_disjoint_splitting = CN_USE_DS;
    }
    else
    {
        std::string value = element->GetText();
        if(value.compare("true") == 0 || value.compare("1") == 0)
        {
            use_disjoint_splitting = true;
        }
        else if(value.compare("false") == 0 || value.compare("0") == 0)
        {
            use_disjoint_splitting = false;
        }
        else
        {
            std::cout << "Error! Wrong 'use_disjoint_splitting' element found inside '"<<CNS_TAG_ALGORITHM<<"' section. It's compared to '"<<CN_USE_DS<<"'."<<std::endl;
            LOG_WARNING("Error! Wrong 'use_disjoint_splitting' element found inside '{}' section. It's compared to '{}'.");
            use_disjoint_splitting = CN_USE_DS;
        }
    }

    element = algorithm->FirstChildElement("connectedness");
    if (!element)
    {
        LOG_WARNING("Error! No 'connectedness' element found inside '{}' section. It's compared to '{}'.", CNS_TAG_ALGORITHM, CN_CONNECTEDNESS);
        connectdness = CN_CONNECTEDNESS;
    }
    else
    {
        auto value = element->GetText();
        stream<<value;
        stream>>connectdness;
        if(connectdness > 5 || connectdness < 2)
        {
            LOG_WARNING("Error! Wrong 'connectedness' value found inside '{}' section. It's compared to '{}'.", CNS_TAG_ALGORITHM, CN_CONNECTEDNESS);
            connectdness = CN_CONNECTEDNESS;
        }
        stream.clear();
        stream.str("");
    }

    element = algorithm->FirstChildElement("focal_weight");
    if (!element)
    {
        LOG_WARNING("Error! No 'focal_weight' element found inside '{}' section. It's compared to '{}'.", CNS_TAG_ALGORITHM, CN_FOCAL_WEIGHT);
        focal_weight = CN_FOCAL_WEIGHT;
    }
    else
    {
        auto value = element->GetText();
        stream<<value;
        stream>>focal_weight;
        if(focal_weight < 1.0)
        {
            LOG_WARNING("Error! Wrong 'focal_weight' value found inside '{}' section. It's compared to '{}'.", CNS_TAG_ALGORITHM, CN_FOCAL_WEIGHT);
            focal_weight = CN_FOCAL_WEIGHT;
        }
        stream.clear();
        stream.str("");
    }

    element = algorithm->FirstChildElement("agent_size");
    if (!element)
    {
        LOG_WARNING("Error! No 'agent_size' element found inside '{}' section. It's compared to '{}'.", CNS_TAG_ALGORITHM, CN_AGENT_SIZE);
        agent_size = CN_AGENT_SIZE;
    }
    else
    {
        auto value = element->GetText();
        stream<<value;
        stream>>agent_size;
        if(agent_size < 0 || agent_size > 0.5)
        {
            LOG_WARNING("Error! Wrong 'agent_size' value found inside '{}' section. It's compared to '{}'.", CNS_TAG_ALGORITHM, CN_AGENT_SIZE);
            agent_size = CN_AGENT_SIZE;
        }
        stream.clear();
        stream.str("");
    }

    element = algorithm->FirstChildElement("hlh_type");
    if (!element)
    {
        LOG_WARNING("Error! No 'hlh_type' element found inside '{}' section. It's compared to '{}'.", CNS_TAG_ALGORITHM, CN_HLH_TYPE);
        hlh_type = CN_HLH_TYPE;
    }
    else
    {
        auto value = element->GetText();
        stream<<value;
        stream>>hlh_type;
        if(hlh_type < 0 || hlh_type > 2)
        {
            LOG_WARNING("Error! Wrong 'hlh_type' value found inside '{}' section. It's compared to '{}'.", CNS_TAG_ALGORITHM, CN_HLH_TYPE);
            hlh_type = CN_HLH_TYPE;
        }
        stream.clear();
        stream.str("");
    }

    element = algorithm->FirstChildElement("timelimit");
    if (!element)
    {
        LOG_WARNING("Error! No 'timelimit' element found inside '{}' section. It's compared to '{}'.", CNS_TAG_ALGORITHM, CN_TIMELIMIT);
        timelimit = CN_TIMELIMIT;
    }
    else
    {
        auto value = element->GetText();
        stream<<value;
        stream>>timelimit;
        if(timelimit <= 0)
            timelimit = CN_INFINITY;
        stream.clear();
        stream.str("");
    }
    return;
}
