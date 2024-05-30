#ifndef LOGGING_MACROS_H
#define LOGGING_MACROS_H

#include <boost/log/trivial.hpp>
#include <fmt/core.h>

// Helper function to handle variadic arguments with fmt::format
template <typename... Args>
std::string fmt::format(const std::string& message, Args&&... args) {
    return fmt::format(message, std::forward<Args>(args)...);
}

// Define logging macros for different severity levels
#define LOG_TRACE(message, ...) BOOST_LOG_TRIVIAL(trace) << fmt::format(message, ##__VA_ARGS__)
#define LOG_DEBUG(message, ...) BOOST_LOG_TRIVIAL(debug) << fmt::format(message, ##__VA_ARGS__)
#define LOG_INFO(message, ...) BOOST_LOG_TRIVIAL(info) << fmt::format(message, ##__VA_ARGS__)
#define LOG_WARNING(message, ...) BOOST_LOG_TRIVIAL(warning) << fmt::format(message, ##__VA_ARGS__)
#define LOG_ERROR(message, ...) BOOST_LOG_TRIVIAL(error) << fmt::format(message, ##__VA_ARGS__)
#define LOG_FATAL(message, ...) BOOST_LOG_TRIVIAL(fatal) << fmt::format(message, ##__VA_ARGS__)

#endif // LOGGING_MACROS_H