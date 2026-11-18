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
from smoke_checks.commands import check_command_parsing_is_strict
from smoke_checks.environment import check_environment_is_portable_and_secret_free
from smoke_checks.local import (
    check_a_credential_or_an_installed_path_is_a_fact_and_never_prose,
    check_a_destination_outside_its_tree_is_refused,
    check_a_finding_the_code_check_threw_out_is_never_an_ask,
    check_a_home_or_temporary_path_is_refused_on_anybodys_machine,
    check_a_minor_issue_is_never_a_required_revision,
    check_a_missing_engine_fails_the_skill_check_in_ci,
    check_a_row_that_rules_on_another_review_is_refused,
    check_a_severity_this_release_cannot_sort_is_refused,
    check_a_withheld_run_with_no_reason_is_reported_as_having_none,
    check_a_path_shaped_key_is_refused_rather_than_published_without_it,
    check_a_schema_pattern_means_what_the_repositorys_own_gate_means,
    check_a_rehearsal_claims_no_reading,
    check_a_review_that_read_the_code_publishes_the_code_and_not_the_copy,
    check_a_version_is_only_recorded_when_it_looks_like_one,
    check_a_rehearsal_is_never_written_into_the_published_tree,
    check_an_attestation_needs_a_named_editor,
    check_an_unclaimed_review_is_labelled_an_experiment,
    check_every_documented_command_runs_against_a_real_parser,
    check_every_published_file_is_hashed,
    check_every_spelling_of_a_machine_fact_is_the_same_fact,
    check_the_fixtures_counts_are_the_ones_the_reader_computes,
    check_no_editorial_page_names_the_machine_it_was_written_on,
    check_no_published_document_overstates_what_the_editor_agent_did,
    check_nothing_reaches_into_the_engines_internals,
    check_only_this_machines_own_names_are_refused_as_this_machine,
    check_ordinary_review_text_publishes_and_a_local_path_does_not,
    check_the_advisory_verdict_is_labelled_advisory,
    check_the_attestation_says_what_it_has_to_say,
    check_the_citation_section_prints_no_charge_nobody_made,
    check_the_decision_is_attributed_to_a_person,
    check_the_engines_pdf_converter_is_named_before_a_run_and_installed_in_ci,
    check_the_issues_are_split_by_severity_and_ordered_by_rank,
    check_the_letter_marks_a_quote_in_the_line_it_reads_on,
    check_the_locked_engine_commit_is_the_one_declared,
    check_the_method_paragraph_describes_the_run_that_happened,
    check_the_page_keeps_the_model_asked_apart_from_the_model_that_ran,
    check_the_run_fixture_is_a_run_the_engine_could_have_written,
    check_the_skill_commands_match_the_engine_parser,
    run_engine_backed_checks,
)
from smoke_checks.planning import (
    check_a_new_draft_is_planned_as_its_own_review,
    check_rerun_refuses_a_moved_draft,
    check_restamping_is_not_staleness,
    check_round_is_not_version,
    check_slug_uniqueness,
    check_staleness_scan_finds_bundles,
    check_versioning,
)
from smoke_checks.sources import (
    check_a_rate_limit_is_waited_out_in_minutes,
    check_a_submitted_code_link_is_only_ever_an_https_one,
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
    check_a_new_draft_is_planned_as_its_own_review()
    print("ok  a review of a new draft is planned as a review of that draft alone")
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
    print("ok  submission issues get one safe preview of the review to run next")
    check_a_submitted_code_link_is_only_ever_an_https_one()
    print("ok  a submitted code link is accepted only as a public https address")
    check_full_text_source_hierarchy()
    print("ok  official full text is preferred and damaged PDF text falls back to OCR")
    check_metadata_fetch_retries_throttling()
    print("ok  a throttled metadata lookup is retried, a missing one is not")
    check_pdf_download_retries_a_flaky_server()
    print("ok  a flaky PDF download is retried too")
    check_a_rate_limit_is_waited_out_in_minutes()
    print("ok  a rate limit is waited out in minutes, within a budget")
    check_command_parsing_is_strict()
    print("ok  editor commands are parsed strictly")
    check_rerun_refuses_a_moved_draft()
    print("ok  a rerun refuses a draft that moved")

    check_the_issues_are_split_by_severity_and_ordered_by_rank()
    print("ok  the engine's issues are split by severity and kept in rank order")
    check_the_decision_is_attributed_to_a_person()
    print("ok  a local review attributes its decision to a human editor")
    check_the_letter_marks_a_quote_in_the_line_it_reads_on()
    print("ok  the letter marks a quote in the line of the manuscript it reads on")
    check_a_minor_issue_is_never_a_required_revision()
    print("ok  severity alone decides what a revision round must fix")
    check_a_severity_this_release_cannot_sort_is_refused()
    print("ok  an issue carrying a severity this release cannot sort is refused")
    check_a_row_that_rules_on_another_review_is_refused()
    print("ok  an issue carrying a ruling on an earlier review is refused by name")
    check_a_finding_the_code_check_threw_out_is_never_an_ask()
    print("ok  an issue resting on a finding the code check threw out is refused")
    check_a_withheld_run_with_no_reason_is_reported_as_having_none()
    print("ok  a run the engine withheld without a reason is reported as having none")
    check_a_credential_or_an_installed_path_is_a_fact_and_never_prose()
    print("ok  a credential and a path inside an installed environment are refused")
    check_no_published_document_overstates_what_the_editor_agent_did()
    print("ok  no authored document claims more of the editor agent than it did")
    check_no_editorial_page_names_the_machine_it_was_written_on()
    print("ok  no editorial page names the machine it was written on")
    check_the_fixtures_counts_are_the_ones_the_reader_computes()
    print("ok  the fixture's own tallies are the ones the publish path counts")
    check_an_unclaimed_review_is_labelled_an_experiment()
    print("ok  an unclaimed local review is published as an experiment")
    check_every_published_file_is_hashed()
    print("ok  the local bundle manifest hashes every file but itself")
    check_the_attestation_says_what_it_has_to_say()
    print("ok  the published attestation names the transport and the editor")
    check_the_skill_commands_match_the_engine_parser()
    print("ok  every engine command in the skill is one the engine's parser accepts")
    check_every_documented_command_runs_against_a_real_parser()
    print("ok  every command and flag the documents give is one a real parser accepts")
    check_a_rehearsal_is_never_written_into_the_published_tree()
    print("ok  a run without --publish stays out of docs/reviews")
    check_the_method_paragraph_describes_the_run_that_happened()
    print("ok  the summary describes the run that was recorded")
    check_the_page_keeps_the_model_asked_apart_from_the_model_that_ran()
    print("ok  the page shows each slot's model asked and model ran, from two fields")
    check_the_citation_section_prints_no_charge_nobody_made()
    print("ok  the citations section states each lookup state and sums none of them")
    check_a_review_that_read_the_code_publishes_the_code_and_not_the_copy()
    print("ok  a review that read the code publishes the code read and not the copy taken")
    check_an_attestation_needs_a_named_editor()
    print("ok  a true attestation needs a named editor and an actual reading")
    check_a_rehearsal_claims_no_reading()
    print("ok  a rehearsal's documents claim no reading that did not happen")
    check_a_destination_outside_its_tree_is_refused()
    print("ok  a bundle is written only inside the tree it belongs to")
    check_a_missing_engine_fails_the_skill_check_in_ci()
    print("ok  the skill command check fails in CI rather than skipping itself")
    check_the_engines_pdf_converter_is_named_before_a_run_and_installed_in_ci()
    print("ok  the preflight names the engine's PDF converter and CI installs it")
    check_the_advisory_verdict_is_labelled_advisory()
    print("ok  the engine's verdict is published and labelled advisory")
    check_nothing_reaches_into_the_engines_internals()
    print("ok  every engine name these scripts use is on the package's own surface")
    check_ordinary_review_text_publishes_and_a_local_path_does_not()
    print("ok  ordinary review notation publishes and a local path is refused by name")
    check_only_this_machines_own_names_are_refused_as_this_machine()
    print("ok  this machine's own names are refused and ordinary prose is not")
    check_a_home_or_temporary_path_is_refused_on_anybodys_machine()
    print("ok  a home or temporary path is refused whoever's machine it is on")
    check_every_spelling_of_a_machine_fact_is_the_same_fact()
    print("ok  every encoding of a machine fact reduces to the same fact")
    check_a_path_shaped_key_is_refused_rather_than_published_without_it()
    print("ok  a path used as a field name is refused, not dropped with its value")
    check_a_schema_pattern_means_what_the_repositorys_own_gate_means()
    print("ok  a schema pattern is read the way the repository's own gate reads it")
    check_the_run_fixture_is_a_run_the_engine_could_have_written()
    print("ok  the run fixtures are shaped the way the engine writes a run")
    check_a_version_is_only_recorded_when_it_looks_like_one()
    print("ok  a version is recorded only when the probe answered with one")

    run_engine_backed_checks()

    assert slugify("") == "", "empty title should yield an empty slug"
    assert slugify("!!!") == "", "punctuation-only title should yield an empty slug"
    print(f"\n{len(NASTY_TITLES)} fixture bundle(s) written cleanly")

    # Last, because it asserts a fact about requirements.in and requirements.txt
    # rather than about any code here: the two files have to name the same
    # engine commit, and the lock has to carry that archive's hash.
    check_the_locked_engine_commit_is_the_one_declared()
    print("ok  the lock pins the engine release requirements.in declares")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
