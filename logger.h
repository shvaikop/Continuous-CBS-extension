#ifndef LOGGER_HPP
#define LOGGER_HPP
#pragma once

#include <boost/log/core.hpp>
#include <boost/log/trivial.hpp>
#include <boost/log/expressions.hpp>
#include <boost/log/utility/setup/file.hpp>
#include <boost/log/utility/setup/console.hpp>
#include <boost/log/utility/setup/common_attributes.hpp>
#include <boost/log/sources/severity_logger.hpp>
#include <boost/log/sources/record_ostream.hpp>
#include <boost/date_time/posix_time/posix_time.hpp> // for time-based naming
#include <iomanip> // for std::put_time


std::string generate_log_file_name(const std::string& directory) {
    auto t = boost::posix_time::second_clock::local_time();
    std::stringstream ss;

    ss << directory << "/log_"
       << t.date().year() << "_"
       << std::setw(2) << std::setfill('0') << t.date().month().as_number() << "_"
       << std::setw(2) << std::setfill('0') << t.date().day().as_number() << "_"
       << std::setw(2) << std::setfill('0') << t.time_of_day().hours() << "_"
       << std::setw(2) << std::setfill('0') << t.time_of_day().minutes() << "_"
       << std::setw(2) << std::setfill('0') << t.time_of_day().seconds()
       << ".log";
    return ss.str();
}

void init_logging() {

    // Set up file logging
    std::string log_file_name = generate_log_file_name("logs");
    // boost::log::add_file_log(
    //     boost::log::keywords::file_name = log_file_name, // Log files named sample_1.log, sample_2.log, etc.
    //     boost::log::keywords::format = "[%TimeStamp%]: %Message%"
    // );

    boost::log::add_file_log(
        boost::log::keywords::file_name = log_file_name, // Log files named sample_1.log, sample_2.log, etc.
        // boost::log::keywords::format = "[%TimeStamp%]: %Message%"
        boost::log::keywords::filter = boost::log::trivial::severity >= boost::log::trivial::info,
        boost::log::keywords::format = (
            boost::log::expressions::stream
                << "[" << boost::log::expressions::attr<boost::posix_time::ptime>("TimeStamp") << "]"
                << " <" << boost::log::trivial::severity << "> "
                << boost::log::expressions::format_named_scope("Scope", boost::log::keywords::format = "%n")
                << " - " << boost::log::expressions::smessage
        )
    );

    // Set up console sink for warnings and errors
    boost::log::add_console_log(
        std::clog,
        boost::log::keywords::filter = boost::log::trivial::severity >= boost::log::trivial::warning,
        boost::log::keywords::format = (
            boost::log::expressions::stream
                << "[" << boost::log::expressions::attr<boost::posix_time::ptime>("TimeStamp") << "]"
                << " <" << boost::log::trivial::severity << "> "
                << boost::log::expressions::smessage
        )
    );

    // Set a filter to only log messages with severity >= info
    boost::log::core::get()->set_filter(
        boost::log::trivial::severity >= boost::log::trivial::info
    );

    // Add common attributes like timestamp
    boost::log::add_common_attributes();
}

#endif /* LOGGER_HPP */