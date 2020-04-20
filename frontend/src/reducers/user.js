import {GET_USERS, IS_LOGGED_IN} from "../actions/types";


const initialState = {
    isLoggedIn: false,
    usersList: []
};

export default function(state = initialState, action) {
    switch(action.type){
        case IS_LOGGED_IN:
            return {
                ...state,
                isLoggedIn: action.payload
            };
        case GET_USERS:
            return {
                ...state,
                usersList: [...action.payload]
            };
        default:
            return state;
    }
}