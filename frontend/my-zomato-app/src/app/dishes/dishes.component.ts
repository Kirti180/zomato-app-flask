import { Component, OnInit } from '@angular/core';
import { NgForm } from '@angular/forms';
import { DishesService } from '../services/dishes.service';

@Component({
  selector: 'app-dishes',
  templateUrl: './dishes.component.html',
  styleUrls: ['./dishes.component.css']
})
export class DishesComponent implements OnInit {
  dishes: any[] = [];
  newDish: any = {
    name: '',
    price: null,
    availability: false
  };
  selectedDish: any = {
    _id: '',
    name: '',
    price: null,
    availability: false
  };
  isModalOpen: boolean = false;

  constructor(private dishesService: DishesService) { }

  ngOnInit(): void {
    this.getDishes();
  }

  getDishes(): void {
    this.dishesService.getDishes().subscribe(
      (response: any) => {
        this.dishes = response;
      },
      (error: any) => {
        console.error('Error fetching dishes:', error);
      }
    );
  }

  createDish(dishForm: NgForm): void {
    if (dishForm.valid) {
      this.dishesService.createDish(this.newDish).subscribe(
        (response: any) => {
          console.log('Dish created successfully:', response);
          this.getDishes();
          this.newDish = {
            name: '',
            price: null,
            availability: false
          };
          dishForm.resetForm();
        },
        (error: any) => {
          console.error('Error creating dish:', error);
        }
      );
    }
  }

  updateDish(dish: any): void {
    this.selectedDish = { ...dish };
    this.openModal();
  }

  saveChanges(): void {
    const dishData = { ...this.selectedDish };
    delete dishData._id;

    this.dishesService.updateDish(dishData).subscribe(
      (response: any) => {
        console.log('Dish updated successfully:', response);
        this.closeModal();
        this.getDishes();
      },
      (error: any) => {
        console.error('Error updating dish:', error);
      }
    );
  }

  deleteDish(dishId: number): void {
    this.dishesService.deleteDish(dishId).subscribe(
      (response: any) => {
        console.log('Dish deleted successfully:', response);
        this.getDishes();
      },
      (error: any) => {
        console.error('Error deleting dish:', error);
      }
    );
  }

  openModal() {
    this.isModalOpen = true;
  }

  closeModal() {
    this.isModalOpen = false;
  }
}
