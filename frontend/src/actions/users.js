import {IS_LOGGED_IN, GET_USERS} from "./types";
import axios from 'axios';

export const setIsLoggedIn = (payload) => ({
    type: IS_LOGGED_IN,
    payload
});

export const setUsers = () => dispatch => {

    axios.get('http://localhost:8000/api/user/')
        .then(res => {
            console.log(res);
            dispatch({
                type: GET_USERS,
                payload: res.data
            })
        })
};