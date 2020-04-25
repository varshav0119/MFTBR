import { Component, OnInit } from '@angular/core';
import { FormGroup, FormControl, Validators } from '@angular/forms';

import { HttpClient, HttpParams } from '@angular/common/http';
import { ActivatedRoute } from '@angular/router';
import { Pipe, PipeTransform } from '@angular/core';


@Component({
  selector: 'app-model',
  templateUrl: './model.component.html',
  styleUrls: ['./model.component.css']
})
export class ModelComponent implements OnInit {

  iduser;
  idproduct;
  response;
  predictUrl: string;
  
  constructor(private http: HttpClient, private route: ActivatedRoute) {
    this.predictUrl = "http://localhost:5000/model/predict";
    this.route.params.subscribe( params => {
      console.log("Parameters: ", params);
      this.iduser = params.iduser;
      this.idproduct = params.idproduct;
    } );
   }

  ngOnInit(): void {
    let params = {"iduser": this.iduser, "idproduct": this.idproduct};
    this.http.get(this.predictUrl, { params: params }).subscribe( data => 
      {
        console.log("Response: ", data)
        this.response = data
      });
  }
}
