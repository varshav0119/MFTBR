import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { Product } from './product';

@Injectable({
  providedIn: 'root'
})
export class ProductService {

  productUrl: "localhost:5000/products"

  constructor(private http: HttpClient) { }

  getProducts() {
    return this.http.get<Product[]>(this.productUrl);
  }
}
