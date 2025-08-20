from app.repositories.customer_repository import CustomerRepository
from app.schemas.customer_in import CustomerIn
from app.views.customer_with_account_out import CustomerWithAccountOut


class CustomerService:

    def __init__(self, repository: CustomerRepository):
        self.repository = repository

    async def get_customers(self, limit, skip) -> list[CustomerWithAccountOut]:
        return await self.repository.get_customers(limit=limit, skip=skip)

    async def get_custumer(self, id) -> CustomerWithAccountOut:
        return await self.repository.find_by_id(id)

    async def create_customer(self, post: CustomerIn) -> CustomerWithAccountOut:
        return await self.repository.create_customer(post)