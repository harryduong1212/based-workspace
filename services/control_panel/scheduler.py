"""APScheduler integration for Routines.

This module provides a BackgroundScheduler that runs within the FastAPI app.
It loads enabled routines from SQLite on startup and provides a sync method
to update the scheduler when routines are modified via the API.
"""
from __future__ import annotations

import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from . import db
from .config import Config
from .recipes_index import get_recipe
from .runs import start_run

log = logging.getLogger(__name__)

_scheduler = BackgroundScheduler()


def _execute_routine(cfg: Config, routine_id: str) -> None:
    """The actual job function executed by APScheduler."""
    routine = db.get_routine(routine_id)
    if not routine or not routine.enabled:
        return
        
    result = get_recipe(cfg, routine.recipe_id)
    if not result:
        log.warning("Routine %s attempted to run missing recipe %s", routine_id, routine.recipe_id)
        return
        
    fm, body, _path = result
    
    # We do not block APScheduler waiting for the run; start_run spins up its own daemon thread.
    start_run(cfg, routine.recipe_id, fm, body, routine.inputs, routine.model_ref)
    log.info("Dispatched routine %s (recipe: %s)", routine_id, routine.recipe_id)


def init(cfg: Config) -> None:
    """Start the background scheduler and load all enabled routines."""
    if _scheduler.running:
        return
        
    # Schedule all currently enabled routines
    for routine in db.list_routines():
        if routine.enabled:
            _add_job(cfg, routine)
            
    _scheduler.start()


def _add_job(cfg: Config, routine: db.RoutineRow) -> None:
    try:
        _scheduler.add_job(
            _execute_routine,
            CronTrigger.from_crontab(routine.schedule),
            args=[cfg, routine.id],
            id=routine.id,
            replace_existing=True,
        )
    except Exception as e:
        log.error("Failed to schedule routine %s with cron %r: %s", routine.id, routine.schedule, e)


def sync_routine(cfg: Config, routine_id: str) -> None:
    """Sync a specific routine from DB into the running scheduler.
    Call this after upserting or deleting a routine in SQLite."""
    routine = db.get_routine(routine_id)
    
    if not routine or not routine.enabled:
        if _scheduler.get_job(routine_id):
            _scheduler.remove_job(routine_id)
        return
        
    _add_job(cfg, routine)


def shutdown() -> None:
    """Gracefully stop the scheduler."""
    if _scheduler.running:
        _scheduler.shutdown(wait=False)
