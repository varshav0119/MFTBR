import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class ModelService {

  modelUrl: 'localhost:5000/model'

  constructor(private http: HttpClient) { }

  getModel(iduser: number, idproduct: number){
    // console.warn("hi");
    console.warn(iduser, idproduct);
    let params = new HttpParams().set('iduser', String(iduser)).set('idproduct', String(idproduct));
    console.warn(params);
    return this.http.get(this.modelUrl, {params});
    // {params: params}
  }
}
