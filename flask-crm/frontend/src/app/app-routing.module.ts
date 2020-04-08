import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { TempComponent } from './temp/temp.component';


const routes: Routes = [
  { path: 'home', component: HomeComponent },
  { path: 'temp', component: TempComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
