//reducer is a function that takes in an action and evaluates the action then sends down a state based on the action evaluation
import { GET_PRODUCTS, DELETE_PRODUCT, ADD_PRODUCT } from '../actions/types.js';
import {UPDATE_PRODUCTS} from "../actions/types";

const initialState = {
    products: []
};

export default function(state = initialState, action) {
    switch(action.type){
        case GET_PRODUCTS:
            return {
                ...state,
                products: action.payload
            };
        case DELETE_PRODUCT:
            return {
                ...state,
                products: state.products.filter(product => product.id !== action.payload)
            };
        case ADD_PRODUCT:
            return {
                ...state,
                products: [...state.products, action.payload]
            };
        case UPDATE_PRODUCTS:
            return {
                ...state,
                products: [...action.payload]
            };
        default:
            return state;
    }
}