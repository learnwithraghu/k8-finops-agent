# Manifests

Contains the airline deployment manifests used in section 02.

## Services

| Service | Namespace | Port | Purpose |
|---------|-----------|------|---------|
| **booking-api** | booking-api | 8080 | Flight booking UI + mock API (Skyscanner-style wizard) |
| **flight-search-service** | flight-search | 80 | Flight search (mock nginx) |
| **payment-processor** | payment | 8443 | Payment processing (mock nginx) |
| **inventory-service** | inventory | 8080 | Seat inventory (mock nginx) |
| **analytics-collector** | default | 80 | Analytics collection |

## Accessing the Booking UI

After deployment, access the Skyscanner-style UI at `http://localhost:8080`:

```bash
kubectl port-forward -n booking-api svc/booking-api 8080:8080 --address 127.0.0.1
```

The booking API serves a 5-step flight booking wizard:
1. **Search** — Select origin, destination, date, passengers
2. **Results** — Choose from mock flight options
3. **Details** — Enter passenger information
4. **Payment** — Card form with live preview
5. **Confirmation** — Booking ID + transaction details

All API calls return mock data from nginx config — no backend services required.
