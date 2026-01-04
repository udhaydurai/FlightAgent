"""Open-jaw flight search utilities for multi-city trips."""
from typing import Dict, Any, List, Optional
from api.services.amadeus_client import AmadeusClient
from api.utils.config import (
    get_origin,
    get_destinations,
    get_open_jaw_options,
    get_dates
)


class OpenJawSearch:
    """Handle open-jaw flight searches (fly into one city, out of another)."""
    
    def __init__(self):
        """Initialize with Amadeus client."""
        self.client = AmadeusClient()
        self.origin = get_origin()
        self.destinations = get_destinations()
        self.open_jaw_options = get_open_jaw_options()
    
    def search_all_open_jaw_options(
        self,
        departure_date: str,
        return_date: str,
        adults: int = 1
    ) -> Dict[str, Any]:
        """
        Search for all open-jaw itinerary options.
        
        Searches both:
        1. SAN → WAS, NYC → SAN
        2. SAN → NYC, WAS → SAN
        
        Args:
            departure_date: Outbound departure date (YYYY-MM-DD)
            return_date: Return departure date (YYYY-MM-DD)
            adults: Number of adult passengers
        
        Returns:
            Dictionary with results for both open-jaw options
        """
        results = {
            "success": True,
            "options": []
        }
        
        for option in self.open_jaw_options:
            inbound_city = option.get("inbound")
            outbound_city = option.get("outbound")
            
            # Get airport codes for inbound city
            inbound_airports = self.destinations.get(inbound_city, [])
            # Get airport codes for outbound city
            outbound_airports = self.destinations.get(outbound_city, [])
            
            option_results = []
            
            # Search all combinations of airports
            for inbound_airport in inbound_airports:
                for outbound_airport in outbound_airports:
                    # Search outbound: SAN → Inbound City
                    outbound_result = self.client.search_flights_filtered(
                        origin=self.origin,
                        destination=inbound_airport,
                        departure_date=departure_date,
                        adults=adults
                    )
                    
                    # Search return: Outbound City → SAN
                    return_result = self.client.search_flights_filtered(
                        origin=outbound_airport,
                        destination=self.origin,
                        departure_date=return_date,
                        adults=adults
                    )
                    
                    if outbound_result["success"] and return_result["success"]:
                        option_results.append({
                            "inbound_airport": inbound_airport,
                            "outbound_airport": outbound_airport,
                            "description": option.get("description", ""),
                            "outbound_flights": {
                                "count": len(outbound_result.get("data", [])),
                                "offers": outbound_result.get("data", [])[:5]  # Top 5
                            },
                            "return_flights": {
                                "count": len(return_result.get("data", [])),
                                "offers": return_result.get("data", [])[:5]  # Top 5
                            },
                            "combined_options": self._combine_flights(
                                outbound_result.get("data", []),
                                return_result.get("data", [])
                            )
                        })
            
            results["options"].append({
                "inbound_city": inbound_city,
                "outbound_city": outbound_city,
                "description": option.get("description", ""),
                "airport_combinations": option_results
            })
        
        return results
    
    def _combine_flights(
        self,
        outbound_flights: List[Dict[str, Any]],
        return_flights: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Combine outbound and return flights into complete trip options.
        
        Args:
            outbound_flights: List of outbound flight offers
            return_flights: List of return flight offers
        
        Returns:
            List of combined trip options with total price
        """
        combined = []
        
        for outbound in outbound_flights[:10]:  # Limit combinations
            for return_flight in return_flights[:10]:
                outbound_price = self._extract_price(outbound)
                return_price = self._extract_price(return_flight)
                total_price = outbound_price + return_price
                
                combined.append({
                    "outbound": outbound,
                    "return": return_flight,
                    "total_price": total_price,
                    "currency": outbound.get("price", {}).get("currency", "USD")
                })
        
        # Sort by total price
        combined.sort(key=lambda x: x["total_price"])
        return combined[:20]  # Return top 20 combinations
    
    def _extract_price(self, flight_offer: Dict[str, Any]) -> float:
        """Extract price from flight offer."""
        price_info = flight_offer.get("price", {})
        total = price_info.get("total", "0")
        try:
            return float(total)
        except (ValueError, TypeError):
            return 0.0
    
    def search_best_open_jaw(
        self,
        departure_date: str,
        return_date: str,
        adults: int = 1
    ) -> Dict[str, Any]:
        """
        Find the best open-jaw itinerary option.
        
        Args:
            departure_date: Outbound departure date (YYYY-MM-DD)
            return_date: Return departure date (YYYY-MM-DD)
            adults: Number of adult passengers
        
        Returns:
            Dictionary with the best open-jaw option
        """
        all_results = self.search_all_open_jaw_options(
            departure_date=departure_date,
            return_date=return_date,
            adults=adults
        )
        
        if not all_results["success"]:
            return all_results
        
        best_option = None
        best_price = float('inf')
        
        for option_group in all_results["options"]:
            for combo in option_group.get("airport_combinations", []):
                for combined in combo.get("combined_options", []):
                    price = combined.get("total_price", float('inf'))
                    if price < best_price:
                        best_price = price
                        best_option = {
                            "inbound_airport": combo["inbound_airport"],
                            "outbound_airport": combo["outbound_airport"],
                            "description": combo["description"],
                            "outbound_flight": combined["outbound"],
                            "return_flight": combined["return"],
                            "total_price": price,
                            "currency": combined["currency"]
                        }
        
        return {
            "success": True,
            "best_option": best_option,
            "all_options": all_results
        }
