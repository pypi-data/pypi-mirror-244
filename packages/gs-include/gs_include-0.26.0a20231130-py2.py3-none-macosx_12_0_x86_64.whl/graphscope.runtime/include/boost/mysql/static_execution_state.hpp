//
// Copyright (c) 2019-2023 Ruben Perez Hidalgo (rubenperez038 at gmail dot com)
//
// Distributed under the Boost Software License, Version 1.0. (See accompanying
// file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
//

#ifndef BOOST_MYSQL_STATIC_EXECUTION_STATE_HPP
#define BOOST_MYSQL_STATIC_EXECUTION_STATE_HPP

#include <boost/mysql/detail/config.hpp>

#ifdef BOOST_MYSQL_CXX14

#include <boost/mysql/metadata.hpp>
#include <boost/mysql/metadata_collection_view.hpp>
#include <boost/mysql/string_view.hpp>

#include <boost/mysql/detail/access.hpp>
#include <boost/mysql/detail/execution_processor/static_execution_state_impl.hpp>

namespace boost {
namespace mysql {

/**
 * \brief Holds state for multi-function SQL execution operations (static interface).
 * \details
 * This class behaves like a state machine. The current state can be accessed using
 * \ref should_start_op, \ref should_read_rows, \ref should_read_head
 * and \ref complete. They are mutually exclusive.
 * More states may be added in the future as more protocol features are implemented.
 * \n
 * Note that this class doesn't store rows anyhow. Row template parameters are
 * used to validate their compatibility with the data that will be returned by the server.
 *
 * \tparam StaticRow The row or row types that will be returned by the server.
 * There must be one for every resultset returned by the query, and always at least one.
 * All the passed types must fulfill the `StaticRow` concept.
 *
 * \par Thread safety
 * Distinct objects: safe. \n
 * Shared objects: unsafe.
 */
template <class... StaticRow>
class static_execution_state
{
public:
    /**
     * \brief Default constructor.
     * \details The constructed object is guaranteed to have
     * `should_start_op() == true`.
     *
     * \par Exception safety
     * No-throw guarantee.
     */
    static_execution_state() = default;

    /**
     * \brief Copy constructor.
     * \par Exception safety
     * Strong guarantee. Internal allocations may throw.
     *
     * \par Object lifetimes
     * `*this` lifetime will be independent of `other`'s.
     */
    static_execution_state(const static_execution_state& other) = default;

    /**
     * \brief Move constructor.
     * \par Exception safety
     * No-throw guarantee.
     *
     * \par Object lifetimes
     * Views obtained from `other` remain valid.
     */
    static_execution_state(static_execution_state&& other) = default;

    /**
     * \brief Copy assignment.
     * \par Exception safety
     * Basic guarantee. Internal allocations may throw.
     *
     * \par Object lifetimes
     * `*this` lifetime will be independent of `other`'s. Views obtained from `*this`
     * are invalidated.
     */
    static_execution_state& operator=(const static_execution_state& other) = default;

    /**
     * \brief Move assignment.
     * \par Exception safety
     * No-throw guarantee.
     *
     * \par Object lifetimes
     * Views obtained from `*this` are invalidated. Views obtained from `other` remain valid.
     */
    static_execution_state& operator=(static_execution_state&& other) = default;

    /**
     * \brief Returns whether `*this` is in the initial state.
     * \details
     * Call \ref connection::start_execution or \ref connection::async_start_execution to move
     * forward. No data is available in this state.
     *
     * \par Exception safety
     * No-throw guarantee.
     */
    bool should_start_op() const noexcept { return impl_.get_interface().is_reading_first(); }

    /**
     * \brief Returns whether the next operation should be read resultset head.
     * \details
     * Call \ref connection::read_resultset_head or its async counterpart to move forward.
     * Metadata and OK data for the previous resultset is available in this state.
     *
     * \par Exception safety
     * No-throw guarantee.
     */
    bool should_read_head() const noexcept { return impl_.get_interface().is_reading_first_subseq(); }

    /**
     * \brief Returns whether the next operation should be read some rows.
     * \details
     * Call \ref connection::read_some_rows or its async counterpart to move forward.
     * Metadata for the current resultset is available in this state.
     *
     * \par Exception safety
     * No-throw guarantee.
     */
    bool should_read_rows() const noexcept { return impl_.get_interface().is_reading_rows(); }

    /**
     * \brief Returns whether all the messages generated by this operation have been read.
     * \details
     * No further network calls are required to move forward. Metadata and OK data for the last
     * resultset are available in this state.
     *
     * \par Exception safety
     * No-throw guarantee.
     */
    bool complete() const noexcept { return impl_.get_interface().is_complete(); }

    /**
     * \brief Returns metadata about the columns in the query.
     * \details
     * The returned collection will have as many \ref metadata objects as columns retrieved by
     * the SQL query, and in the same order. Note that this may not be the same order as in the `StaticRow`
     * type, since columns may be mapped by name or discarded. This function returns the representation that
     * was retrieved from the database.
     *
     * \par Exception safety
     * No-throw guarantee.
     *
     * \par Object lifetimes
     * This function returns a view object, with reference semantics. The returned view points into
     * memory owned by `*this`, and will be valid as long as `*this` or an object move-constructed
     * from `*this` are alive.
     */
    metadata_collection_view meta() const noexcept { return impl_.get_interface().meta(); }

    /**
     * \brief Returns the number of rows affected by the SQL statement associated to this resultset.
     * \par Exception safety
     * No-throw guarantee.
     *
     * \par Preconditions
     * `this->complete() == true || this->should_read_head() == true`
     */
    std::uint64_t affected_rows() const noexcept { return impl_.get_interface().get_affected_rows(); }

    /**
     * \brief Returns the last insert ID produced by the SQL statement associated to this resultset.
     * \par Exception safety
     * No-throw guarantee.
     *
     * \par Preconditions
     * `this->complete() == true || this->should_read_head() == true`
     */
    std::uint64_t last_insert_id() const noexcept { return impl_.get_interface().get_last_insert_id(); }

    /**
     * \brief Returns the number of warnings produced by the SQL statement associated to this resultset.
     * \par Exception safety
     * No-throw guarantee.
     *
     * \par Preconditions
     * `this->complete() == true || this->should_read_head() == true`
     */
    unsigned warning_count() const noexcept { return impl_.get_interface().get_warning_count(); }

    /**
     * \brief Returns additional text information about this resultset.
     * \details
     * The format of this information is documented by MySQL <a
     * href="https://dev.mysql.com/doc/c-api/8.0/en/mysql-info.html">here</a>.
     * \n
     * The returned string always uses ASCII encoding, regardless of the connection's character set.
     *
     * \par Exception safety
     * No-throw guarantee.
     *
     * \par Preconditions
     * `this->complete() == true || this->should_read_head() == true`
     *
     * \par Object lifetimes
     * This function returns a view object, with reference semantics. The returned view points into
     * memory owned by `*this`, and will be valid as long as `*this` or an object move-constructed
     * from `*this` are alive.
     */
    string_view info() const noexcept { return impl_.get_interface().get_info(); }

    /**
     * \brief Returns whether the current resultset represents a procedure OUT params.
     * \par Preconditions
     * `this->complete() == true || this->should_read_head() == true`
     *
     * \par Exception safety
     * No-throw guarantee.
     */
    bool is_out_params() const noexcept { return impl_.get_interface().get_is_out_params(); }

private:
    detail::static_execution_state_impl<StaticRow...> impl_;

    static_assert(sizeof...(StaticRow) > 0, "static_execution_state requires one row type, at least");

#ifndef BOOST_MYSQL_DOXYGEN
    friend struct detail::access;
#endif
};

}  // namespace mysql
}  // namespace boost

#endif  // BOOST_MYSQL_CXX14

#endif
