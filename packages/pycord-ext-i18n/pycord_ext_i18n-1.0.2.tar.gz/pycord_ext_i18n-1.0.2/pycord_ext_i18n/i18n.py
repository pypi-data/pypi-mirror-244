import json

from pathlib import Path
from typing import Dict

from .errors import PathNoexists
from .utils import as_valid_locale

class I18n:
    def __init__(self):
        self._dict = {}
        self._paths = set()

    def load(self, _path: str):
        self._dict = {}
        self._paths = set()
        path = Path(_path)
        
        if path.is_file():
            self._load_file(path)
        elif path.is_dir():
            for file in path.glob("*.json"):
                if not file.is_file():
                    continue
                self._load_file(file)
        else:
            raise PathNoexists("Path does not exist or is not a directory/file. Did you enter it correctly?")
        
        self._paths.add(path)
    
    def _load_file(self, path: Path) -> None:
        try:
            if path.suffix != ".json":
                raise ValueError("not a .json file")
            locale = path.stem

            if not (api_locale := as_valid_locale(locale)):
                raise ValueError(f"invalid locale '{locale}'")
            locale = api_locale

            data = json.loads(path.read_text("utf-8"))
            self._load_dict(data, locale)
        except Exception as e:
            raise RuntimeError(f"Unable to load '{path}': {e}") from e

    def _load_dict(self, data: Dict[str, str], locale: str) -> None:
        if not isinstance(data, dict) or not all(
            o is None or isinstance(o, str) for o in data.values()
        ):
            raise TypeError("data must be a flat dict with string/null values")
        for key, value in data.items():
            d = self._dict  # always create dict, regardless of value
            if value is not None:
                d[key] = {locale: value}
    
    def get(self, key: str):
        """Returns localizations for the specified key.

        Parameters
        ----------
        key: :class:`str`
            The lookup key.

        Returns
        -------
        Optional[Dict[:class:`str`, :class:`str`]]
            The localizations for the provided key.
            Returns ``None`` if no localizations could be found and :attr:`strict` is disabled.
        """
        data = self._dict.get(key)
        if data is None:
            return None
        return data 
        
    def get_text(self, key: str, locale: str, default = None):
        """
        Gets a text from i18n files by key
        :param key: The key of the text
        :param locale: The locale of the text
        :param default: The default value to return if the text is not found
        :return: The text
        """ 
        return self.get(key).get(locale, default) 
    