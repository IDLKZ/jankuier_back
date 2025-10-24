"""
Централизованное хранилище констант для Redis ключей.
Обеспечивает консистентность именования ключей во всем приложении.
"""


class AppRedisKeys:
    """Константы для Redis ключей приложения"""

    # === SOTA Service Keys ===
    SOTA_ACCESS_TOKEN = "sota_access_token"

    # Префиксы для SOTA данных
    SOTA_COUNTRIES_PREFIX = "sota_countries"
    SOTA_TOURNAMENTS_PREFIX = "sota_tournaments"
    SOTA_MATCHES_PREFIX = "sota_matches"
    SOTA_SCORE_TABLE_PREFIX = "sota_score_table"
    SOTA_TEAM_STAT_PREFIX = "sota_team_stat"
    SOTA_PLAYERS_STAT_PREFIX = "sota_players_stat"
    SOTA_LINEUP_PREFIX = "sota_lineup"

    # === Ticketon Service Keys ===
    TICKETON_SHOWS_PREFIX = "ticketon_shows"
    TICKETON_SINGLE_SHOW_PREFIX = "ticketon_single_show"
    TICKETON_SHOW_LEVEL_PREFIX = "ticketon_show_level"
    TICKETON_LEVEL_PREFIX = "ticketon_level"

    @staticmethod
    def sota_countries_key(lang: str, **params) -> str:
        """
        Генерирует ключ для кеширования стран SOTA.

        Args:
            lang: Язык локализации
            **params: Дополнительные параметры (page, page_size и т.д.)

        Returns:
            str: Redis ключ
        """
        param_str = "_".join(f"{k}_{v}" for k, v in sorted(params.items()) if v is not None)
        if param_str:
            return f"{AppRedisKeys.SOTA_COUNTRIES_PREFIX}_{lang}_{param_str}"
        return f"{AppRedisKeys.SOTA_COUNTRIES_PREFIX}_{lang}"

    @staticmethod
    def sota_tournaments_key(lang: str, **params) -> str:
        """
        Генерирует ключ для кеширования турниров SOTA.

        Args:
            lang: Язык локализации
            **params: Дополнительные параметры (country, page и т.д.)

        Returns:
            str: Redis ключ
        """
        param_str = "_".join(f"{k}_{v}" for k, v in sorted(params.items()) if v is not None)
        if param_str:
            return f"{AppRedisKeys.SOTA_TOURNAMENTS_PREFIX}_{lang}_{param_str}"
        return f"{AppRedisKeys.SOTA_TOURNAMENTS_PREFIX}_{lang}"

    @staticmethod
    def sota_matches_key(lang: str, tournament_id: int | None = None, season_id: int | None = None) -> str:
        """
        Генерирует ключ для кеширования матчей SOTA.

        Args:
            lang: Язык локализации
            tournament_id: ID турнира
            season_id: ID сезона

        Returns:
            str: Redis ключ
        """
        parts = [AppRedisKeys.SOTA_MATCHES_PREFIX, lang]
        if tournament_id:
            parts.append(f"tournament_{tournament_id}")
        if season_id:
            parts.append(f"season_{season_id}")
        return "_".join(parts)

    @staticmethod
    def sota_score_table_key(lang: str, season_id: int) -> str:
        """
        Генерирует ключ для кеширования турнирной таблицы SOTA.

        Args:
            lang: Язык локализации
            season_id: ID сезона

        Returns:
            str: Redis ключ
        """
        return f"{AppRedisKeys.SOTA_SCORE_TABLE_PREFIX}_{lang}_{season_id}"

    @staticmethod
    def sota_team_stat_key(lang: str, game_id: str) -> str:
        """
        Генерирует ключ для кеширования статистики команд SOTA.

        Args:
            lang: Язык локализации
            game_id: ID игры

        Returns:
            str: Redis ключ
        """
        return f"{AppRedisKeys.SOTA_TEAM_STAT_PREFIX}_{lang}_{game_id}"

    @staticmethod
    def sota_players_stat_key(lang: str, game_id: str) -> str:
        """
        Генерирует ключ для кеширования статистики игроков SOTA.

        Args:
            lang: Язык локализации
            game_id: ID игры

        Returns:
            str: Redis ключ
        """
        return f"{AppRedisKeys.SOTA_PLAYERS_STAT_PREFIX}_{lang}_{game_id}"

    @staticmethod
    def sota_lineup_key(lang: str, game_id: str) -> str:
        """
        Генерирует ключ для кеширования составов SOTA.

        Args:
            lang: Язык локализации
            game_id: ID игры

        Returns:
            str: Redis ключ
        """
        return f"{AppRedisKeys.SOTA_LINEUP_PREFIX}_{lang}_{game_id}"

    @staticmethod
    def ticketon_shows_key(event_type: str | None, places: list[int] | None,
                          with_param: str | None, i18n: str | None) -> str:
        """
        Генерирует ключ для кеширования событий Ticketon.

        Args:
            event_type: Тип события
            places: Список мест проведения
            with_param: Временной параметр
            i18n: Язык локализации

        Returns:
            str: Redis ключ
        """
        parts = [AppRedisKeys.TICKETON_SHOWS_PREFIX]
        if event_type:
            parts.append(f"type_{event_type}")
        if places:
            parts.append(f"places_{'_'.join(map(str, places))}")
        if with_param:
            parts.append(f"with_{with_param}")
        if i18n:
            parts.append(f"lang_{i18n}")
        return "_".join(parts)

    @staticmethod
    def ticketon_single_show_key(show_id: int, i18n: str | None = "ru") -> str:
        """
        Генерирует ключ для кеширования одного события Ticketon.

        Args:
            show_id: ID события
            i18n: Язык локализации

        Returns:
            str: Redis ключ
        """
        return f"{AppRedisKeys.TICKETON_SINGLE_SHOW_PREFIX}_{show_id}_{i18n}"
