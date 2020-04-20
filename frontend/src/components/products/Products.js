import React, { useState } from "react";
import {connect, useDispatch} from "react-redux";
import PropTypes from "prop-types";
import {getProducts, deleteProduct, setProductList} from "../../actions/products";
import axios from 'axios';

const buildSearchObj = () => {
    let searchObj = {}
    if($('#name-search').val() && $('#name-search').val().trim() != ''){
        searchObj.name = $('#name-search').val().trim();
    }
    if($('#desc-search').val() && $('#desc-search').val().trim() != ''){
        searchObj.description = $('#desc-search').val().trim();
    }
    if($('#quantity-search').val() && $('#quantity-search').val().trim() != ''){
        searchObj.quantity = $('#quantity-search').val().trim();
    }
    if($('#category-search').val() && $('#category-search').val().trim() != ''){
        searchObj.category = $('#category-search').val().trim();
    }
    if($('#name-price').val() && $('#price-search').val().trim() != ''){
        searchObj.price = $('#price-search').val().trim();
    }

    return searchObj
};

const searchProducts = (dispatch) => {
    const searchRequest = buildSearchObj()

    if(Object.keys(searchRequest).length !== 0){
        axios.post('http://localhost:8000/api/products/search/', searchRequest)
            .then(res => {
                dispatch(setProductList(res.data));
            })
    }
};

export const Products = (props) => {

    const dispatch = useDispatch();
    const [isLoaded, setIsLoaded] = useState(false);


    if(!isLoaded) {
        dispatch(getProducts());
        setIsLoaded(true);
    }

    return (
        <div>
            <h2>Products</h2>
            <table className="table table-striped">
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Description</th>
                        <th>Category</th>
                        <th>Price</th>
                        <th>Quantity</th>
                        <th>
                            <button className={'btn btn-outline-success'} onClick={() => dispatch(getProducts())}>
                                Refresh List
                            </button>
                        </th>
                        <th />
                    </tr>
                    {
                        props.products.products.length > 0 ?
                            <tr>
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
                                        id={'desc-search'}
                                        className={'form-control'}
                                        placeholder={'Search description'}
                                    />
                                </td>
                                <td>
                                    <input
                                        type={'text'}
                                        id={'category-search'}
                                        className={'form-control'}
                                        placeholder={'Search category'}
                                    />
                                </td>
                                <td>
                                    <input
                                        type={'text'}
                                        id={'price-search'}
                                        className={'form-control'}
                                        placeholder={'Search price'}
                                    />
                                </td>
                                <td>
                                    <input
                                        type={'text'}
                                        id={'quantity-search'}
                                        className={'form-control'}
                                        placeholder={'Search quantity'}
                                    />
                                </td>
                                <td>
                                    <button
                                        id={'search-btn'}
                                        className={'btn btn-outline-primary'}
                                        placeholder={'Search'}
                                        onClick={() => searchProducts(dispatch)}
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
                    { props.products.products.map(product => (
                        <tr key= {product.id}>
                            <td>{product.name}</td>
                            <td>{product.description}</td>
                            <td>{product.category}</td>
                            <td>{product.price}</td>
                            <td>{product.quantity}</td>
                            <td>
                                <button onClick={() => dispatch(deleteProduct)} className="btn btn-danger btn-sm">
                                    Delete
                                </button>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}

const mapStateToProps = state => ({
    products: state.products
});

export default connect(mapStateToProps)(Products);
