#define BOOST_LOG_DYN_LINK 1

#include <iostream>
#include <fstream>
#include <sstream>
#include "map.h"
#include "task.h"
#include "cbs.h"
#include "xml_logger.h"
#include "logger.h"
#include "logger_macros.h"


int main(int argc, const char *argv[])
{
    if(argc > 2)
    {
        init_logging();
        LOG_INFO("Start CBS {}", "Algorithm");
        Config config;
        if(argc > 3)
            config.getConfig(argv[3]);
        Map map = Map(config.agent_size, config.connectdness);
        map.get_map(argv[1]);
        Task task;
        task.get_task(argv[2]);
        if(map.is_roadmap())
            task.make_ij(map);
        else
            task.make_ids(map.get_width());
        CBS cbs;
        Solution solution = cbs.find_solution(map, task, config);
        XML_logger logger;
        auto found = solution.found?"true":"false";
        std::cout<< "Soulution found: " << found << "\nRuntime: "<<solution.time.count() << "\nMakespan: " << solution.makespan << "\nFlowtime: " << solution.flowtime<< "\nInitial Cost: "<<solution.init_cost<< "\nCollision Checking Time: " << solution.check_time
             << "\nHL expanded: " << solution.high_level_expanded << "\nLL searches: " << solution.low_level_expansions << "\nLL expanded(avg): " << solution.low_level_expanded << std::endl;

        logger.get_log(argv[2]);
        logger.write_to_log_summary(solution);
        logger.write_to_log_path(solution, map);
        logger.save_log();
    }
    else
    {
        std::cout<<"Error! Not enough input parameters are specified!\n";
    }
    return 0;
}
