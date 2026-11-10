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
from smoke_checks.local import (
    check_a_bare_pdf_cannot_be_published,
    check_a_dated_model_id_is_not_a_substitution,
    check_a_destination_outside_its_tree_is_refused,
    check_a_minor_finding_is_never_a_required_revision,
    check_a_missing_engine_fails_the_skill_check_in_ci,
    check_a_published_record_names_no_local_path,
    check_a_rehearsal_claims_no_reading,
    check_a_rehearsal_is_never_written_into_the_published_tree,
    check_a_run_of_one_paper_cannot_be_published_as_another,
    check_a_run_with_no_manifest_paper_id_is_still_bound,
    check_a_subscription_login_is_not_a_paid_provider,
    check_a_substituted_model_is_visible,
    check_an_attestation_needs_a_named_editor,
    check_an_unclaimed_review_is_labelled_an_experiment,
    check_an_unfinished_run_cannot_be_published,
    check_every_published_file_is_hashed,
    check_provenance_is_read_from_the_run,
    check_publishing_needs_a_verified_login,
    check_severity_is_read_from_the_engine_not_guessed,
    check_the_attestation_says_what_it_has_to_say,
    check_the_decision_is_attributed_to_a_person,
    check_the_locked_engine_release_contains_the_engine,
    check_the_method_paragraph_describes_the_run_that_happened,
    check_the_model_comes_from_the_run_not_the_flag,
    check_the_skill_commands_match_the_engine_parser,
    check_the_synthesis_record_is_read_where_the_engine_writes_it,
)
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

    check_severity_is_read_from_the_engine_not_guessed()
    print("ok  an unrecognised severity stays visible and out of the counts")
    check_the_decision_is_attributed_to_a_person()
    print("ok  a local review attributes its decision to a human editor")
    check_a_minor_finding_is_never_a_required_revision()
    print("ok  severity alone decides what a revision round must fix")
    check_an_unclaimed_review_is_labelled_an_experiment()
    print("ok  an unclaimed local review is published as an experiment")
    check_every_published_file_is_hashed()
    print("ok  the local bundle manifest hashes every file but itself")
    check_a_bare_pdf_cannot_be_published()
    print("ok  a review of an unidentified PDF cannot be published")
    check_the_attestation_says_what_it_has_to_say()
    print("ok  the published attestation names the transport and the editor")
    check_a_subscription_login_is_not_a_paid_provider()
    print("ok  a subscription login passes the preflight and a paid one does not")
    check_the_skill_commands_match_the_engine_parser()
    print("ok  every engine command in the skill is one the engine's parser accepts")
    check_provenance_is_read_from_the_run()
    print("ok  the provenance record is read from what the run wrote")
    check_a_run_of_one_paper_cannot_be_published_as_another()
    print("ok  a run is bound to the paper that was prepared")
    check_a_rehearsal_is_never_written_into_the_published_tree()
    print("ok  a run without --publish stays out of docs/reviews")
    check_a_substituted_model_is_visible()
    print("ok  a model the transport substituted is read from the usage receipts")
    check_the_method_paragraph_describes_the_run_that_happened()
    print("ok  the summary describes the run that was recorded")
    check_an_attestation_needs_a_named_editor()
    print("ok  a true attestation needs a named editor and an actual reading")
    check_the_model_comes_from_the_run_not_the_flag()
    print("ok  the published model is the one the run asked for")
    check_a_run_with_no_manifest_paper_id_is_still_bound()
    print("ok  a run that records its paper id outside the manifest is still bound")
    check_an_unfinished_run_cannot_be_published()
    print("ok  a run that did not finish cannot be published")
    check_a_dated_model_id_is_not_a_substitution()
    print("ok  model drift uses the engine's own rule for the same model")
    check_a_published_record_names_no_local_path()
    print("ok  a published record names no path on the operator's disk")
    check_publishing_needs_a_verified_login()
    print("ok  publishing needs a login that was actually checked")
    check_the_synthesis_record_is_read_where_the_engine_writes_it()
    print("ok  the synthesis policy and its budget are read from the stage folder")
    check_a_rehearsal_claims_no_reading()
    print("ok  a rehearsal's documents claim no reading that did not happen")
    check_a_destination_outside_its_tree_is_refused()
    print("ok  a bundle is written only inside the tree it belongs to")
    check_a_missing_engine_fails_the_skill_check_in_ci()
    print("ok  the skill command check fails in CI rather than skipping itself")
    check_the_locked_engine_release_contains_the_engine()
    print("ok  the locked release contains the engine the checks import")

    assert slugify("") == "", "empty title should yield an empty slug"
    assert slugify("!!!") == "", "punctuation-only title should yield an empty slug"
    print(f"\n{len(NASTY_TITLES)} fixture bundle(s) written cleanly")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
