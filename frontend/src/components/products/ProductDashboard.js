import React, { Fragment } from 'react';
import Form from './Form';
import Products from './Products';

export default function ProductDashboard() {
    return (
        <div className={'container'}>
            <Form/>
            <Products/>
        </div>
    )
}

