def update_info(session, resources_manager, buildings_resources_manager, facilities_manager, research_manager, defenses_manager, shipyard_manager):
    resources_manager.updateResourcesInfo(session)
    buildings_resources_manager.updateResourcesBuildingsInfo(session)
    facilities_manager.updateFacilitiesInfo(session)
    research_manager.updateResearchesInfo(session)
    defenses_manager.updateDefensesInfo(session)
    shipyard_manager.updateShipyardInfo(session)
    