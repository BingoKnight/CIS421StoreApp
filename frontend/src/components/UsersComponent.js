import React, { useState } from 'react';
import {connect, useDispatch} from 'react-redux';
import $ from 'jquery';
import { setUsers } from "../actions/users";


const searchUsers = dispatch => {
//    build out search like products
}

const UsersComponent = (props) => {

    const dispatch = useDispatch();
    const [isLoaded, setIsLoaded] = useState(false);

    if(!isLoaded){
        dispatch(setUsers());
        setIsLoaded(true);
    }

    return (
        <div className={'container'}>
            <table className="table table-striped">
                <thead>
                <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Email</th>
                    <th>
                        <button className={'btn btn-outline-success'} onClick={() => dispatch(setUsers())}>
                            Refresh List
                        </button>
                    </th>
                    <th />
                </tr>
                {
                    props.users.length > 0 ?
                        <tr>
                            <td>
                                <input
                                    type={'text'}
                                    id={'id-search'}
                                    className={'form-control'}
                                    placeholder={'Search ID'}
                                />
                            </td>
                            <td>
                                <input
                                    type={'text'}
                                    id={'name-search'}
                                    className={'form-control'}
                                    placeholder={'Search name'}
                                />
                            </td>
                            <td>
                                <input
                                    type={'text'}
                                    id={'email-search'}
                                    className={'form-control'}
                                    placeholder={'Search email'}
                                />
                            </td>
                            <td>
                                <button
                                    id={'search-btn'}
                                    className={'btn btn-outline-primary'}
                                    placeholder={'Search'}
                                    onClick={() => searchUsers(dispatch)}
                                >
                                    Search
                                </button>
                            </td>
                        </tr>
                        :
                        null
                }
                </thead>
                <tbody>
                { props.users.map(user => (
                    <tr key= {user.id}>
                        <td>{user.id}</td>
                        <td>{user.name}</td>
                        <td>{user.email}</td>
                    </tr>
                ))}
                </tbody>
            </table>
        </div>
    )
};

const mapStateToProps = state => ({
    users: state.users.usersList
})

export default connect(mapStateToProps)(UsersComponent)