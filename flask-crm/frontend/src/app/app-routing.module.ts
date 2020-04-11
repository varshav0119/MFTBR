import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { TempComponent } from './temp/temp.component';
import { ModelComponent } from './model/model.component';


const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'temp', component: TempComponent },
  { path: 'model', component: ModelComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
