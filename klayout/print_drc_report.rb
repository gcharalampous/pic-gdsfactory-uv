# klayout/print_drc_summary.rb
include RBA

report_path = (ENV["REPORT"] || "").strip
abort("Set REPORT env var to the .lyrdb path (REPORT=/path/to/report.lyrdb)") if report_path.empty?

rdb = ReportDatabase::new
rdb.load(report_path)

def walk_categories(cat, out)
  # Recurse into sub-categories; if none, treat as leaf category.
  has_sub = false
  begin
    cat.each_sub_category do |sub|
      has_sub = true
      walk_categories(sub, out)
    end
  rescue
    # If each_sub_category is not available for some reason, fall back to leaf.
    has_sub = false
  end

  unless has_sub
    # For leaf categories, num_items should correspond to that rule's violations
    out << [cat.path, cat.num_items]
  end
end

counts = []
rdb.each_category do |top|
  walk_categories(top, counts)
end

total = rdb.num_items
puts "DRC SUMMARY: #{total} total violations"

# Print top 20 rules by count
counts.sort_by { |(_name, n)| -n }.first(20).each do |name, n|
  puts format("%6d  %s", n, name)
end

# Exit code: 0 if clean, 2 if violations exist (nice for CI)
exit(total == 0 ? 0 : 2)
