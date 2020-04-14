import {IS_LOGGED_IN} from "./types";

export const setIsLoggedIn = (payload) => ({
    type: IS_LOGGED_IN,
    payload
});