document.addEventListener("DOMContentLoaded", () => {
  const activitiesList = document.getElementById("activities-list");
  const activitySelect = document.getElementById("activity");
  const signupForm = document.getElementById("signup-form");
  const messageDiv = document.getElementById("message");

  // Utility to escape HTML (prevent injection from participant emails)
  function escapeHtml(str) {
    return String(str).replace(/[&<>"']/g, (s) => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[s]));
  }

  // Function to fetch activities from API
  async function fetchActivities() {
    try {
      const response = await fetch("/activities");
      const activities = await response.json();

      // Clear loading message and previous options
      activitiesList.innerHTML = "";
      activitySelect.innerHTML = '<option value="">-- Select an activity --</option>';

      // Populate activities list
      Object.entries(activities).forEach(([name, details]) => {
        const activityCard = document.createElement("div");
        activityCard.className = "activity-card";

        const spotsLeft = details.max_participants - details.participants.length;

        // Build participants HTML (no bullets, add remove 'X' button)
        const participantsHTML = details.participants.length
          ? details.participants.map(p => `
              <span class="participant-item">
                <span class="participant-pill">${escapeHtml(p)}</span>
                <button class="remove-participant" data-email="${encodeURIComponent(p)}" title="Remove participant">×</button>
              </span>
            `).join('')
          : '<p class="no-participants">No participants yet</p>';

        activityCard.innerHTML = `
          <h4>${escapeHtml(name)}</h4>
          <p>${escapeHtml(details.description)}</p>
          <p><strong>Schedule:</strong> ${escapeHtml(details.schedule)}</p>
          <p><strong>Availability:</strong> ${spotsLeft} spots left</p>

          <div class="participants-section">
            <button class="toggle-participants">Show participants (${details.participants.length})</button>
            <div class="participants hidden">
              ${participantsHTML}
            </div>
          </div>
        `;

        activitiesList.appendChild(activityCard);

        // Add toggle behavior for participants
        const toggleBtn = activityCard.querySelector(".toggle-participants");
        const participantsDiv = activityCard.querySelector(".participants");
        toggleBtn.addEventListener("click", () => {
          const isHidden = participantsDiv.classList.toggle("hidden");
          toggleBtn.textContent = `${isHidden ? "Show" : "Hide"} participants (${details.participants.length})`;
        });

        // Add remove handlers for each participant (the 'X' button)
        const removeButtons = activityCard.querySelectorAll(".remove-participant");
        removeButtons.forEach(btn => {
          btn.addEventListener("click", async (e) => {
            e.stopPropagation();
            const emailEncoded = btn.dataset.email;
            const email = decodeURIComponent(emailEncoded);
            if (!confirm(`Remove ${email} from ${name}?`)) return;
            try {
              const res = await fetch(`/activities/${encodeURIComponent(name)}/participants?email=${emailEncoded}`, {
                method: "DELETE",
              });
              const result = await res.json();
              if (res.ok) {
                messageDiv.textContent = result.message;
                messageDiv.className = "success";
                fetchActivities();
              } else {
                messageDiv.textContent = result.detail || "An error occurred";
                messageDiv.className = "error";
              }
              messageDiv.classList.remove("hidden");
              setTimeout(() => {
                messageDiv.classList.add("hidden");
              }, 5000);
            } catch (error) {
              messageDiv.textContent = "Failed to remove participant. Please try again.";
              messageDiv.className = "error";
              messageDiv.classList.remove("hidden");
              console.error("Error removing participant:", error);
            }
          });
        });

        // Add option to select dropdown
        const option = document.createElement("option");
        option.value = name;
        option.textContent = name;
        activitySelect.appendChild(option);
      });
    } catch (error) {
      activitiesList.innerHTML = "<p>Failed to load activities. Please try again later.</p>";
      console.error("Error fetching activities:", error);
    }
  }

  // Handle form submission
  signupForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const email = document.getElementById("email").value;
    const activity = document.getElementById("activity").value;

    try {
      const response = await fetch(
        `/activities/${encodeURIComponent(activity)}/signup?email=${encodeURIComponent(email)}`,
        {
          method: "POST",
        }
      );

      const result = await response.json();

      if (response.ok) {
        messageDiv.textContent = result.message;
        messageDiv.className = "success";
        signupForm.reset();

        // Refresh activities so participants and counts update
        fetchActivities();
      } else {
        messageDiv.textContent = result.detail || "An error occurred";
        messageDiv.className = "error";
      }

      messageDiv.classList.remove("hidden");

      // Hide message after 5 seconds
      setTimeout(() => {
        messageDiv.classList.add("hidden");
      }, 5000);
    } catch (error) {
      messageDiv.textContent = "Failed to sign up. Please try again.";
      messageDiv.className = "error";
      messageDiv.classList.remove("hidden");
      console.error("Error signing up:", error);
    }
  });

  // Initialize app
  fetchActivities();
});
