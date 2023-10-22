from core.config._main import AppConfig

CONFIG_SWAGGER_TRUE = {
    "title": "ChensonUz",
    "docs_url": "/docs",
    "redoc_url": "/redoc",
    "swagger_ui_parameters": {"operationsSorter": "method"},
    "version": "1.0",
    "description": """
        
    """,
    "author": "ChensonUz Dev",
}

CONFIG_SWAGGER_FALSE = {
    "docs_url": None,
    "redoc_url": None,
}


def get_swagger_config() -> dict:
    return CONFIG_SWAGGER_TRUE if AppConfig.SHOW_DOCS else CONFIG_SWAGGER_FALSE
