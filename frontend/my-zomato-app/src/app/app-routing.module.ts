import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { DishesComponent } from './dishes/dishes.component';
import { OrdersComponent } from './orders/orders.component';
import { HomeComponent } from './home/home.component';

const routes: Routes = [
  { path: 'dishes', component: DishesComponent },
  { path: 'orders', component: OrdersComponent },
  { path: '', component: HomeComponent },
  { path: '**', redirectTo: '/', pathMatch: 'full' } // Add a wildcard route for handling unknown routes
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
