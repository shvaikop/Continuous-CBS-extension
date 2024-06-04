#include <optional>
#include <structs.h>


inline int get_agent_id_unsafe(opt_agent_ref_t agent) {
	if (!agent.has_value()) {
		return -1;
	}
	return agent->get().id;
}


inline int get_agent_id_safe(opt_agent_ref_t agent) {
	// if (!agent.has_value()) {
	// 	throw std::runtime_error("Agent reference is empty");
	// }
	// int id = agent->get().id;
	// if (id < 0) {
	// 	throw std::runtime_error("Agent id is negative");
	// }
	// return id;
	return get_agent_id_unsafe(agent);
}
