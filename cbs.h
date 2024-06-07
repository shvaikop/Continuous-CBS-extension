#ifndef CBS_H
#define CBS_H
#include <chrono>
#include "structs.h"
#include "map.h"
#include "task.h"
#include "config.h"
#include "sipp.h"
#include "heuristic.h"
#include "logger_macros.h"
#include "simplex/simplex.h"
#include "simplex/pilal.h"

class CBS
{
public:
    CBS(const Map    & map,
        const Task   & task,
        const Config   config);

    Solution find_solution();

private:
    bool init_root();

    std::list<Constraint> get_constraints(CBS_Node * node,
                                          int        agent_id = -1);

    //std::list<Constraint> merge_constraints(std::list<Constraint> constraints);

    bool validate_constraints(std::list<Constraint> constraints, int agent);

    bool check_positive_constraints(std::list<Constraint> constraints, Constraint constraint);

    Conflict check_paths(const sPath &pathA, const sPath &pathB);

    bool check_conflict(Move move1, Move move2);

    double get_hl_heuristic(const std::list<Conflict> &conflicts);

    std::vector<Conflict> get_all_conflicts(const std::vector<sPath> &paths, int id);

    Constraint get_constraint(int agent, Move move1, Move move2);

    Constraint get_wait_constraint(int agent, Move move1, Move move2);

    void find_new_conflicts(CBS_Node                  & node,
                            std::vector<sPath>        & paths,
                            const sPath               & path,
                            const std::list<Conflict> & conflicts,
                            const std::list<Conflict> & semicard_conflicts,
                            const std::list<Conflict> & cardinal_conflicts,
                            int                       & low_level_searches,
                            int                       & low_level_expanded);

    double get_cost(CBS_Node node, int agent_id);

    std::vector<sPath> get_paths(CBS_Node *node, unsigned int agents_size);

    Conflict get_conflict(std::list<Conflict> &conflicts);

    CBS_Tree tree;
    SIPP planner;
    Solution solution;
    Heuristic h_values;
    const Map* map = nullptr;
    const Task* task = nullptr; 
    const Config config;
};

#endif // CBS_H
