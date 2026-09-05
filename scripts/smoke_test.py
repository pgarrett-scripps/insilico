"""Run all hermetic review checks without a model or network access."""
from review_plan import slugify
from smoke_checks.bundles import (
    check,
    check_desk_reject,
    check_manuscript_ingest_is_recorded,
    check_provenance_is_portable_and_secret_free,
    check_published_artifacts_are_preserved,
    check_published_bundle_cannot_be_overwritten,
    check_site_never_injects_raw_html,
    check_solicitation_is_labelled,
    check_unscorable_dimension_is_not_a_good_score,
)
from smoke_checks.commands import (
    check_command_parsing_is_strict,
    check_desk_screen_is_non_enforcing,
    check_one_model_means_one_model,
    check_rerun_does_not_inherit_the_prior_round,
)
from smoke_checks.environment import check_environment_is_portable_and_secret_free
from smoke_checks.planning import (
    check_latest_editorial_attempt_is_the_revision_baseline,
    check_rerun_refuses_a_moved_draft,
    check_restamping_is_not_staleness,
    check_round_is_not_version,
    check_slug_uniqueness,
    check_staleness_scan_finds_bundles,
    check_versioning,
)
from smoke_checks.sources import (
    check_a_rate_limit_is_waited_out_in_minutes,
    check_bare_doi_picks_the_right_server,
    check_download_is_bounded,
    check_full_text_source_hierarchy,
    check_link_forms_a_browser_produces,
    check_metadata_fetch_retries_throttling,
    check_metadata_is_sanitised_at_ingestion,
    check_pdf_download_retries_a_flaky_server,
    check_rejected_sources,
    check_submission_preview,
    check_url_is_canonical,
)
from smoke_checks.support import NASTY_TITLES


def main() -> int:
    check_environment_is_portable_and_secret_free()
    print("ok  environment records contain versions and hashes without secrets")
    for title in NASTY_TITLES:
        check(title)
        print(f"ok  {title}")

    check_unscorable_dimension_is_not_a_good_score()
    print("ok  a dimension that does not apply leaves the mean")
    check_manuscript_ingest_is_recorded()
    print("ok  how the manuscript was read is always recorded")
    check_desk_reject()
    print("ok  desk reject records no panel and keeps every body")
    check_provenance_is_portable_and_secret_free()
    print("ok  provenance is portable and excludes secrets")
    check_published_artifacts_are_preserved()
    print("ok  published reviewer output and metadata are preserved")
    check_published_bundle_cannot_be_overwritten()
    print("ok  published review bundles cannot be overwritten")
    check_versioning()
    print("ok  manuscript versions and immutable review attempts stay separate")
    check_slug_uniqueness()
    print("ok  distinct papers get distinct directories")
    check_staleness_scan_finds_bundles()
    print("ok  the staleness scan finds the layout we write")
    check_restamping_is_not_staleness()
    print("ok  a re-stamped bioRxiv PDF is not reported as stale")
    check_round_is_not_version()
    print("ok  bundle version and review round stay distinct")
    check_latest_editorial_attempt_is_the_revision_baseline()
    print("ok  a revision follows the latest eligible editorial review")
    check_solicitation_is_labelled()
    print("ok  the solicitation claim is recorded, all three ways")
    check_metadata_is_sanitised_at_ingestion()
    print("ok  metadata is stripped of tags where it enters")
    check_site_never_injects_raw_html()
    print("ok  the site never opts out of escaping")
    check_url_is_canonical()
    print("ok  stored URLs are rebuilt, not echoed")
    check_download_is_bounded()
    print("ok  downloads are size-capped")
    check_rejected_sources()
    print("ok  only arXiv / bioRxiv / medRxiv accepted")
    check_link_forms_a_browser_produces()
    print("ok  every browser link form yields the same identifier")
    check_bare_doi_picks_the_right_server()
    print("ok  a bare DOI resolves to the server that actually holds it")
    check_submission_preview()
    print("ok  submission issues get one safe editor command preview")
    check_full_text_source_hierarchy()
    print("ok  official full text is preferred and damaged PDF text falls back to OCR")
    check_desk_screen_is_non_enforcing()
    print("ok  desk screening is temporarily non-enforcing")
    check_metadata_fetch_retries_throttling()
    print("ok  a throttled metadata lookup is retried, a missing one is not")
    check_pdf_download_retries_a_flaky_server()
    print("ok  a flaky PDF download is retried too")
    check_a_rate_limit_is_waited_out_in_minutes()
    print("ok  a rate limit is waited out in minutes, within a budget")
    check_command_parsing_is_strict()
    print("ok  editor commands are parsed strictly")
    check_one_model_means_one_model()
    print("ok  one named model means one model")
    check_rerun_refuses_a_moved_draft()
    print("ok  a rerun refuses a draft that moved")
    check_rerun_does_not_inherit_the_prior_round()
    print("ok  a rerun does not inherit the round it tests")

    assert slugify("") == "", "empty title should yield an empty slug"
    assert slugify("!!!") == "", "punctuation-only title should yield an empty slug"
    print(f"\n{len(NASTY_TITLES)} fixture bundle(s) written cleanly")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
