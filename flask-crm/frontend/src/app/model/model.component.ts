import { Component, OnInit } from '@angular/core';
import { FormGroup, FormControl, Validators } from '@angular/forms';
import { ModelService } from '../model.service';

import { HttpClient, HttpParams } from '@angular/common/http';



@Component({
  selector: 'app-model',
  templateUrl: './model.component.html',
  styleUrls: ['./model.component.css']
})
export class ModelComponent implements OnInit {

  form = new FormGroup({
    iduser: new FormControl(''),
    idproduct: new FormControl(''),
  });

  response;
  
  constructor(private modelService: ModelService, private http: HttpClient) { }

  ngOnInit(): void {
  }

  onSubmit(){
    console.warn(this.form.value);
    this.predict(this.form.get('iduser').value, this.form.get('idproduct').value)

  }

  predict(iduser: number, idproduct: number){
    let params = new HttpParams().set('iduser',String(iduser)).set('idproduct',String(idproduct));
    this.http.get<any>('http://localhost:5000/model', {params}).subscribe( data => { this.response = data})
    // this.modelService.getModel(iduser, idproduct)
    //         .subscribe((data: any) => this.response = data);
    
  }

}
