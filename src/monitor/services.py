from django.db import transaction
from rest_framework.exceptions import NotFound
from datetime import datetime, timedelta

from .models import Product, ProductsPrices


class CalculateAveragePriceService:
    @classmethod
    def calculate_average_price(cls, product_id, start_date, end_date):
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

        if start_date > end_date:
            raise ValueError("start_date cannot be greater than end_date")

        prices = ProductsPrices.objects.filter(
            product_id=product_id,
            start_date__lte=end_date,
            end_date__gte=start_date
        )

        if not prices.exists():
            raise NotFound('No prices found for the specified date range')

        total_price = 0
        total_days = 0

        for price in prices:
            overlap_start = max(price.start_date, start_date)
            overlap_end = min(price.end_date, end_date)
            overlap_days = (overlap_end - overlap_start).days + 1

            total_price += price.price * overlap_days
            total_days += overlap_days

        if total_days > 0:
            average_price = total_price / total_days
        else:
            average_price = 0

        return average_price


class ProductService:
    @classmethod
    def validate_date_range(self, start_date, end_date):
        if end_date > start_date:
            return True

    @classmethod
    @transaction.atomic
    def create_product_with_price(self, name, price, start_date, end_date):
        if end_date and not self.validate_date_range(start_date, end_date):
            raise ValueError("start_date cannot be greater than end_date")

        product = Product.objects.create(name=name)

        if price is not None:
            ProductsPrices.objects.create(
                product=product,
                price=price,
                start_date=start_date,
                end_date=end_date,
            )

        return product

    @classmethod
    @transaction.atomic
    def update_product_with_price(self, instance, price, start_date, end_date):
        if end_date and not self.validate_date_range(start_date, end_date):
            raise ValueError("start_date cannot be greater than end_date")

        instance.name = instance.name

        existing_entry = ProductsPrices.objects.filter(
            product=instance,
            start_date=start_date,
            end_date=end_date
        ).first()

        if existing_entry:
            existing_entry.price = price
            existing_entry.save()
        else:
            if end_date:
                overlapping_entries = ProductsPrices.objects.filter(
                    product=instance,
                    start_date__lte=end_date,
                    end_date__gte=start_date
                )
            else:
                overlapping_entries = ProductsPrices.objects.filter(
                    product=instance,
                    end_date__gte=start_date
                )

            if overlapping_entries.exists():
                raise ValueError('Overlapping date ranges with existing prices.')

            endless_price_range = ProductsPrices.objects.filter(
                product=instance,
                end_date__isnull=True
            ).first()

            if endless_price_range and start_date > endless_price_range.start_date:
                endless_price_range.end_date = start_date - timedelta(days=1)
                endless_price_range.save()

            return ProductsPrices.objects.create(
                product=instance,
                price=price,
                start_date=start_date,
                end_date=end_date,
            )