from core.base_gear import Gear, GearParams
from typing import Dict, Any, List, Tuple
import math

class PlanetaryGearset:
    """Train planétaire"""
    
    def __init__(self, sun: Gear, planets: List[Gear], ring: Gear, 
                 num_planets: int = 3):
        self.sun = sun
        self.planets = planets
        self.ring = ring
        self.num_planets = num_planets
        
        self._validate_gearset()
        self._calculate_ratios()
    
    def _validate_gearset(self):
        """Valider la compatibilité des engrenages"""
        # Vérifier que tous les modules sont identiques
        modules = [self.sun.params.module] + \
                  [p.params.module for p in self.planets] + \
                  [self.ring.params.module]
        
        if len(set(round(m, 3) for m in modules)) > 1:
            raise ValueError("Tous les engrenages doivent avoir le même module")
        
        # Vérifier la condition d'assemblage
        if not self._check_assembly_condition():
            raise ValueError("Condition d'assemblage non satisfaite")
    
    def _check_assembly_condition(self) -> bool:
        """Vérifier la condition d'assemblage des planétaires"""
        N_sun = self.sun.params.teeth
        N_ring = self.ring.params.teeth
        
        # Condition pour un train simple
        condition = (N_sun + N_ring) % self.num_planets == 0
        
        # Condition d'entier pour les distances
        condition_center = (N_sun + self.planets[0].params.teeth) % 1 == 0
        
        return condition and condition_center
    
    def _calculate_ratios(self):
        """Calculer les rapports de transmission"""
        N_sun = self.sun.params.teeth
        N_ring = self.ring.params.teeth
        
        # Rapport planétaire/soleil
        self.planet_sun_ratio = -N_sun / self.planets[0].params.teeth
        
        # Rapport anneau/planétaire
        self.ring_planet_ratio = -self.planets[0].params.teeth / N_ring
        
        # Rapports de transmission typiques
        # Fixe l'anneau, entrée soleil, sortie porte-satellite
        self.fixed_ring_ratio = 1 + (N_ring / N_sun)
        
        # Fixe le soleil, entrée anneau, sortie porte-satellite
        self.fixed_sun_ratio = 1 + (N_sun / N_ring)
        
        # Fixe porte-satellite, entrée soleil, sortie anneau
        self.fixed_carrier_ratio = -N_ring / N_sun
    
    def get_ratio(self, fixed: str, input_: str, output: str) -> float:
        """
        Obtenir le rapport de transmission
        
        Args:
            fixed: Élément fixe ('sun', 'ring', 'carrier')
            input_: Élément d'entrée
            output: Élément de sortie
        """
        ratios = {
            ('ring', 'sun', 'carrier'): self.fixed_ring_ratio,
            ('sun', 'ring', 'carrier'): self.fixed_sun_ratio,
            ('carrier', 'sun', 'ring'): self.fixed_carrier_ratio,
            ('carrier', 'ring', 'sun'): 1 / self.fixed_carrier_ratio,
        }
        
        key = (fixed, input_, output)
        if key in ratios:
            return ratios[key]
        else:
            raise ValueError(f"Combinaison non supportée: {key}")
    
    @property
    def center_distance(self) -> float:
        """Distance entre centres soleil-planétaire"""
        return (self.sun.pitch_diameter + self.planets[0].pitch_diameter) / 2
    
    @property
    def ring_inside_diameter(self) -> float:
        """Diamètre intérieur de l'anneau"""
        return self.ring.root_diameter
    
    def get_info(self) -> Dict[str, Any]:
        """Informations du train planétaire"""
        return {
            'sun_teeth': self.sun.params.teeth,
            'planet_teeth': self.planets[0].params.teeth,
            'ring_teeth': self.ring.params.teeth,
            'num_planets': self.num_planets,
            'fixed_ring_ratio': self.fixed_ring_ratio,
            'fixed_sun_ratio': self.fixed_sun_ratio,
            'fixed_carrier_ratio': self.fixed_carrier_ratio,
            'center_distance': self.center_distance,
            'assembly_condition_met': self._check_assembly_condition()
        }