import { combineReducers } from 'redux';
import products from './products';
import users from './user';

export default combineReducers({
    products,
    users
});