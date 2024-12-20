from unittest.mock import patch, MagicMock

from tests.client_auth_tests import client


def test_get_orders_admin_privileges():
    manager_id = 1
    mock_orders = [
        {"id": 1, "status": "Booked", "client_id": 1, "manager_id": 1},
        {"id": 2, "status": "Completed", "client_id": 2, "manager_id": 1}
    ]

    with patch('app.orders.get_admin_privelegy_by_manager_id', return_value=True), \
            patch('app.orders.get_all_orders', return_value=mock_orders):
        response = client.get(f"/orders/{manager_id}/")

        assert response.status_code == 200
        orders = response.json()
        assert len(orders) == 2
        assert orders[0]["status"] == "Booked"


def test_get_orders_manager_without_admin_privileges():
    manager_id = 2
    mock_orders = [
        {"id": 3, "status": "Booked", "client_id": 3, "manager_id": 2},
        {"id": 4, "status": "Cancelled", "client_id": 4, "manager_id": 2}
    ]

    with patch('app.orders.get_admin_privelegy_by_manager_id', return_value=False), \
            patch('app.orders.get_orders_by_manager_id', return_value=mock_orders):
        response = client.get(f"/orders/{manager_id}/")

        assert response.status_code == 200
        orders = response.json()
        assert len(orders) == 2
        assert orders[1]["status"] == "Cancelled"


def test_update_order_status():
    order_data = {
        "id": 1,
        "status": "Completed"
    }

    with patch('src.repositories.order.get_order_by_id', return_value=MagicMock(id=1, status="Booked", client_id=1)), \
            patch('app.orders.get_client_by_id', return_value=MagicMock(email="client@example.com")), \
            patch('app.orders.get_manager_by_order_id', return_value=MagicMock(name="John", surname="Doe")), \
            patch('app.orders.generate_receipt_service', return_value="fake_pdf"), \
            patch('app.orders.send_email') as mock_send_email:
        response = client.put("/orders/1/status/", json=order_data)

        assert response.status_code == 200
        assert response.json()["message"] == "Order status updated successfully"
        mock_send_email.assert_called_once_with(
            to_address="client@example.com",
            subject="Baraiyq: Order Status Changed By Manager",
            content=(
                "Your Request for creating the order was reviewed by the manager, "
                "and the status has been updated to: COMPLETED.\n\n"
                "Manager: John Doe\n"
                "You can view the details in your dashboard: https://baraiyq.vercel.app/dashboard/my-orders"
            ),
            pdf_attachment="fake_pdf"
        )


def test_update_order_status_not_found():
    order_data = {
        "id": 999,
        "status": "Completed"
    }

    with patch('app.orders.get_order_by_id', return_value=None):
        response = client.put("/orders/999/status/", json=order_data)

        assert response.status_code == 404
        assert response.json()["detail"] == "Order not found"
